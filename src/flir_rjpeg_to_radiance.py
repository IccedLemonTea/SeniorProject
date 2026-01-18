#!/usr/bin/env python3
"""
flir_rjpeg_to_radiance.py

Convert FLIR radiometric JPEG (RJPEG) files to band-integrated spectral
radiance at the sensor using the Planck calibration constants embedded
in the file metadata.

For each input RJPEG, this script:
  1) Extracts the 16-bit raw thermal image (counts) using ExifTool
  2) Reads Planck constants (R1, R2, B, F, O) from metadata
  3) Computes sensor-reaching radiance per pixel:
         L = R1 / (R2 * (Raw + O)) - F
     Units: W·m^-2·sr^-1·µm^-1 (band-integrated over the camera's LWIR band)
  4) Writes TWO outputs:
       - Float32 radiance TIFF:  *_radiance.tif
       - UInt16  raw counts TIFF: *_raw_counts.tif
  5) (Optional) Writes a .npy of the radiance if --npy is specified

Requirements:
  - exiftool (must be on PATH)
  - Python 3.8+
  - pip install pillow numpy imageio

Usage:
  python flir_rjpeg_to_radiance.py /path/to/image.jpg -o /path/to/outdir
  python flir_rjpeg_to_radiance.py /path/to/dir -r -o /path/to/outdir

Notes:
  - If a file lacks the FLIR RawThermalImage tag, the script will skip it.
  - If RawThermalImageType indicates "TemperatureLinear", the script will skip unless --force is provided.
  - RAW counts are saved exactly as 16-bit unsigned values (often 14-bit data stored in 16-bit container).
"""
import argparse
import json
import os
import sys
import subprocess
from io import BytesIO
from typing import Dict, Optional, Tuple, List

import numpy as np
from PIL import Image
import imageio.v3 as iio


PLANCK_TAGS = [
    "PlanckR1", "PlanckR2", "PlanckB", "PlanckF", "PlanckO",
    "RawThermalImageType", "ImageType", "Emissivity",
    "ReflectedApparentTemperature", "AtmosphericTemperature",
    "ObjectDistance", "RelativeHumidity"
]


def run_exiftool_json(path: str, tags: List[str]) -> Dict[str, float]:
    """Run exiftool to fetch tags as JSON (-j -n for numeric where possible)."""
    cmd = ["exiftool", "-j", "-n"] + [f"-{t}" for t in tags] + [path]
    try:
        res = subprocess.run(cmd, capture_output=True, check=True)
    except FileNotFoundError:
        print("ERROR: exiftool not found on PATH. Please install exiftool.", file=sys.stderr)
        sys.exit(2)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: exiftool failed for {path}: {e.stderr.decode(errors='ignore')}", file=sys.stderr)
        return {}
    try:
        data = json.loads(res.stdout.decode("utf-8", errors="ignore"))
        return data[0] if data else {}
    except Exception as e:
        print(f"ERROR: Could not parse exiftool JSON for {path}: {e}", file=sys.stderr)
        return {}


def extract_raw_counts(path: str) -> Optional[np.ndarray]:
    """Extract the embedded RawThermalImage as 16-bit counts array using exiftool -b.
       Returns a numpy uint16 image or None if not available."""
    # Try standard tag first, then explicit group, then fallback EmbeddedImage
    for tag in ("-RawThermalImage", "-FLIR:RawThermalImage", "-EmbeddedImage"):
        cmd = ["exiftool", "-b", tag, path]
        try:
            res = subprocess.run(cmd, capture_output=True, check=True)
        except subprocess.CalledProcessError:
            continue
        except FileNotFoundError:
            print("ERROR: exiftool not found on PATH. Please install exiftool.", file=sys.stderr)
            sys.exit(2)
        blob = res.stdout
        if not blob:
            continue
        # Load via PIL from bytes (should be a 16-bit PNG/TIFF depending on model)
        try:
            im = Image.open(BytesIO(blob))
            arr = np.array(im)
            if arr.dtype != np.uint16:
                arr = arr.astype(np.uint16, copy=False)
            return arr
        except Exception as e:
            # If PIL cannot open, try reading as TIFF with imageio
            try:
                arr = iio.imread(blob, extension=".tiff")
                if arr.dtype != np.uint16:
                    arr = arr.astype(np.uint16, copy=False)
                return arr
            except Exception:
                print(f"WARNING: Failed to decode RawThermalImage from {path}: {e}", file=sys.stderr)
                return None
    return None


def compute_radiance(raw: np.ndarray, R1: float, R2: float, O: float, F: float) -> np.ndarray:
    """Compute sensor-reaching radiance (Float32) from raw counts.
       L = R1 / (R2 * (Raw + O)) - F"""
    raw_f = raw.astype(np.float64)



    """ Reverse the polarity of the raw count image, dark is cool, bright
        is warm"""
    raw_f = (2**16 - 1) - raw_f



    denom = R2 * (raw_f + O)
    bad = denom <= 0
    denom[bad] = np.nan
    L = (R1 / denom) - F
    return L.astype(np.float32)


def looks_temperature_linear(meta: Dict[str, float]) -> bool:
    """Heuristic check for temperature-linear mode based on tags."""
    t = (str(meta.get("RawThermalImageType", "")) + " " + str(meta.get("ImageType", ""))).lower()
    return ("temperature" in t and "linear" in t)


def valid_image_ext(fn: str) -> bool:
    ext = os.path.splitext(fn)[1].lower()
    return ext in (".jpg", ".jpeg", ".rjpg")


def process_file(path: str, outdir: str, force: bool=False, save_npy: bool=False, quiet: bool=False,
                 print_all_values: bool=True) -> Optional[Tuple[str, str]]:
    meta = run_exiftool_json(path, PLANCK_TAGS)
    if not meta:
        if not quiet:
            print(f"Skipping (no metadata): {path}")
        return None

    if looks_temperature_linear(meta) and not force:
        if not quiet:
            print(f"Skipping TemperatureLinear image (use --force to override): {path}")
        return None

    required = ["PlanckR1", "PlanckR2", "PlanckO", "PlanckF"]
    missing = [k for k in required if k not in meta]
    if missing:
        print(f"Skipping (missing {missing}): {path}")
        return None

    raw = extract_raw_counts(path)
    if raw is None:
        print(f"Skipping (no RawThermalImage): {path}")
        return None

    # Compute radiance
    R1 = float(meta["PlanckR1"])
    R2 = float(meta["PlanckR2"])
    O  = float(meta["PlanckO"])
    F  = float(meta["PlanckF"])
    B =  float(meta["PlanckB"])
    L = compute_radiance(raw, R1, R2, O, F)

    # Report out some basic image statistics
    for values, label in zip([raw, L], ["raw", "radiance"]):
        print(f"For the {label} image:")
        print(f"   Min: {values.min()}")
        print(f"   Max: {values.max()}")
        print(f"   Number of non-zero values: {len(np.unique(values[values != 0]))}")
        if print_all_values:
            for value in np.unique(values):
                print(f"{value}")

    base = os.path.splitext(os.path.basename(path))[0]
    os.makedirs(outdir, exist_ok=True)

    out_radiance_tif = os.path.join(outdir, f"{base}_radiance.tif")
    out_raw_tif      = os.path.join(outdir, f"{base}_raw_counts.tif")

    # Save Float32 radiance TIFF
    try:
        iio.imwrite(out_radiance_tif, L.astype(np.float32))
    except Exception as e:
        print(f"ERROR: Failed to write TIFF for {path}: {e}", file=sys.stderr)
        return None

    # Save UInt16 raw counts TIFF
    try:
        raw_u16 = raw.astype(np.uint16, copy=False)
        iio.imwrite(out_raw_tif, raw_u16)
    except Exception as e:
        print(f"ERROR: Failed to write raw-counts TIFF for {path}: {e}", file=sys.stderr)
        return None

    if save_npy:
        npy_path = os.path.join(outdir, f"{base}_radiance.npy")
        try:
            np.save(npy_path, L, allow_pickle=False)
        except Exception as e:
            print(f"WARNING: Failed to write NPY for {path}: {e}", file=sys.stderr)

    return out_radiance_tif, out_raw_tif


def gather_inputs(root: str, recursive: bool) -> List[str]:
    paths = []
    if os.path.isdir(root):
        for dirpath, _, filenames in os.walk(root):
            for fn in filenames:
                fp = os.path.join(dirpath, fn)
                if valid_image_ext(fp):
                    paths.append(fp)
            if not recursive:
                break
    else:
        if valid_image_ext(root):
            paths.append(root)
    return sorted(paths)


def main():
    ap = argparse.ArgumentParser(description="Convert FLIR RJPEG raw counts to sensor radiance (Float32 TIFF), and also write uint16 raw counts TIFF.")
    ap.add_argument("input", help="Path to a FLIR radiometric JPEG (or a directory).")
    ap.add_argument("-o", "--outdir", default=None, help="Output directory (default: alongside input or inside directory).")
    ap.add_argument("-r", "--recursive", action="store_true", help="Recurse into subdirectories when input is a directory.")
    ap.add_argument("--force", action="store_true", help="Process even if file appears to be TemperatureLinear.")
    ap.add_argument("--npy", action="store_true", help="Also save a .npy array of the radiance.")
    ap.add_argument("-q", "--quiet", action="store_true", help="Reduce console output.")
    args = ap.parse_args()

    inputs = gather_inputs(args.input, args.recursive)
    if not inputs:
        print("No RJPEG files found to process.", file=sys.stderr)
        sys.exit(1)

    # Determine output directory behavior
    if args.outdir:
        outdir = args.outdir
        os.makedirs(outdir, exist_ok=True)
    else:
        if os.path.isdir(args.input):
            outdir = os.path.join(args.input, "radiance_out")
            os.makedirs(outdir, exist_ok=True)
        else:
            outdir = os.path.dirname(os.path.abspath(args.input)) or "."

    wrote_any = False
    for p in inputs:
        if not args.quiet:
            print(f"Processing: {p}")
        out = process_file(p, outdir, force=args.force, save_npy=args.npy, quiet=args.quiet)
        if out:
            wrote_any = True
            if not args.quiet:
                rad, raw = out
                print(f"  -> radiance: {rad}")
                print(f"  -> raw     : {raw}")

    if not wrote_any:
        print("Finished, but no outputs were written (files may have been skipped).", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
