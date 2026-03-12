# project_serializer.py
# Hybrid save/load system for the LWIR GUI.
#
# Save layout (one folder per project):
#
#   MyProject/
#   ├── project.json      ← lightweight manifest: paths, UI state, scalars, RSR config
#   └── arrays.npz        ← numpy arrays: coefficients, image_stack, stability_data, rsr (if simulated)
#
# Fixes in this version (v1.1):
#   [1] Full traceback printed to terminal on all errors for every load section
#   [2] Config scalars (directory, BB temp, step, deriv/window params) now read
#       directly from BlackbodyCalibration instance attrs (Option A — stored on
#       self at end of __init__) rather than inferred from GUI state
#   [3] current_image_path now saves mw.list_of_valid_files[mw.index] (a concrete
#       file) rather than mw.item_selected which may be a directory — this was
#       the cause of the "expected str, bytes or os.PathLike, not NoneType" crash

import json
import os
import traceback
import numpy as np
from datetime import datetime
from .pixel_stats import prepare_pixel

PROJECT_SCHEMA_VERSION = "1.1"
MANIFEST_FILENAME      = "project.json"
ARRAYS_FILENAME        = "arrays.npz"


# ══════════════════════════════════════════════════════════════════════════════
#  SAVE
# ══════════════════════════════════════════════════════════════════════════════

def save_project(main_window, folder_path: str) -> None:
    mw = main_window
    os.makedirs(folder_path, exist_ok=True)

    arrays   = {}
    manifest = {
        "schema_version": PROJECT_SCHEMA_VERSION,
        "saved_at":       datetime.now().isoformat(timespec="seconds"),
        "arrays_file":    ARRAYS_FILENAME,
        "files":          {},
        "calibration":    {},
        "NEdT":           {},
        "stability":      {},
        "image":          {},
        "ui":             {},
    }

    # ── 1. File lists & navigation ────────────────────────────────────────────
    manifest["files"] = {
        "list_of_files":     getattr(mw, "list_of_files",     []),
        "item_selected":     getattr(mw, "item_selected",     ""),
        "current_index":     getattr(mw, "index",             None),
        "list_of_image_files": getattr(mw, "list_of_image_files", []),
    }

    # ── 2. Calibration data ───────────────────────────────────────────────────
    cal_data = getattr(mw, "calibration_data", None)
    cal_manifest = {
        "has_coefficients":      False,
        "has_image_stack":       False,
        "rsr_type":              "none",
        "rsr_path":              None,
        "directory":             None,
        "filetype":              "rjpeg",
        "blackbody_temperature": None,
        "temperature_step":      None,
        "environmental_temperature": None,
        "deriv_threshold":       None,
        "window_fraction":       None,
        "_number_of_steps":      None,
        "_array_of_avg_coords": None
    }

    if cal_data is not None:
        if getattr(cal_data, "coefficients", None) is not None:
            arrays["coefficients"]           = cal_data.coefficients
            cal_manifest["has_coefficients"] = True

        if getattr(cal_data, "image_stack", None) is not None:
            arrays["image_stack"]           = cal_data.image_stack
            cal_manifest["has_image_stack"] = True

        # Config scalars are now stored directly on BlackbodyCalibration (Option A).
        for key in ("directory", "filetype", "blackbody_temperature",
                    "temperature_step", "deriv_threshold", "window_fraction", 
                    "environmental_temperature", "_number_of_steps", "_array_of_avg_coords"):
            val = getattr(cal_data, key, None)
            if val is not None:
                cal_manifest[key] = val

        rsr = getattr(cal_data, "rsr", None)
        if isinstance(rsr, np.ndarray):
            arrays["rsr"]            = rsr
            cal_manifest["rsr_type"] = "ndarray"
        elif isinstance(rsr, str) and rsr:
            cal_manifest["rsr_type"] = "path"
            cal_manifest["rsr_path"] = rsr


    manifest["calibration"] = cal_manifest

    # ── 3. NEdT Data ───────────────────────────────────────────────────
    NEdT_manifest = {
            "coefficients_used":      None,
            "image_stack_used":       None,
            "rsr_type":              None,
            "rsr_path":              None,
            "directory":             None,
            "filetype":              None,
            "blackbody_temperature": None,
            "temperature_step":      None,
            "environmental_temperature": None
        }
    NEdT_Data = getattr(mw,"NEdT_Data",None)
    if NEdT_Data is not None:
        arrays["NEdT_Data"] = NEdT_Data
        NEdT_manifest = {
            "coefficients_used":      cal_manifest["has_coefficients"],
            "image_stack_used":       cal_manifest["has_image_stack"],
            "rsr_type":              cal_manifest["rsr_type"],
            "rsr_path":              cal_manifest["rsr_path"],
            "directory":             cal_manifest["directory"],
            "filetype":              "rjpeg",
            "blackbody_temperature": cal_manifest["blackbody_temperature"],
            "temperature_step":      cal_manifest["temperature_step"],
            "environmental_temperature": cal_manifest["environmental_temperature"]
        }

    manifest["NEdT"] = NEdT_manifest

    # ── 4. Stability data ─────────────────────────────────────────────────────
    stab = getattr(mw, "stability_data", None)
    if stab is not None:
        arrays["stability_data"]                    = stab
        manifest["stability"]["has_stability_data"] = True
        manifest["stability"]["stability_var_name"] = "placeholder"
    else:
        manifest["stability"]["has_stability_data"] = False

    # ── 5. Current image path ─────────────────────────────────────────────────
    # FIX [3]: item_selected may be a directory. Use list_of_valid_files[index]
    # to get a concrete file path for ImageDataFactory on load.
    current_file_path = ""
    list_of_valid_files = getattr(mw, "list_of_valid_files", [])
    index             = getattr(mw, "index", None)
    item_selected     = getattr(mw, "item_selected", "")

    if (list_of_valid_files and index is not None
            and 0 <= index < len(list_of_valid_files)):
        candidate = list_of_valid_files[index]
        if os.path.isfile(candidate):
            current_file_path = candidate

    if not current_file_path and os.path.isfile(item_selected):
        current_file_path = item_selected

    manifest["image"] = {"current_image_path": current_file_path}

    # ── 6. UI state ───────────────────────────────────────────────────────────
    manifest["ui"] = {
        "active_tab_index": mw.ui.tabWidget.currentIndex(),
        "tab_enabled": {
            "imageTab":     mw.ui.tabWidget.isTabEnabled(
                                mw.ui.tabWidget.indexOf(mw.ui.imageTab)),
            "calTab":       mw.ui.tabWidget.isTabEnabled(
                                mw.ui.tabWidget.indexOf(mw.ui.calTab)),
            "nedtTab":      mw.ui.tabWidget.isTabEnabled(
                                mw.ui.tabWidget.indexOf(mw.ui.nedtTab)),
            "stabilityTab": mw.ui.tabWidget.isTabEnabled(
                                mw.ui.tabWidget.indexOf(mw.ui.stabilityTab)),
        },
        "frame_slider_value": mw.ui.frameSelection.value(),
        "row_text":           mw.ui.rowTextEdit.toPlainText(),
        "col_text":           mw.ui.colTextEdit.toPlainText(),
    }

    # ── Write ─────────────────────────────────────────────────────────────────
    with open(os.path.join(folder_path, MANIFEST_FILENAME), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    if arrays:
        np.savez_compressed(os.path.join(folder_path, ARRAYS_FILENAME), **arrays)

    print(f"\n[ProjectSerializer] Saved → {folder_path}")
    _print_save_summary(manifest, arrays)


def _print_save_summary(manifest: dict, arrays: dict):
    cal  = manifest.get("calibration", {})
    stab = manifest.get("stability",   {})
    img  = manifest.get("image",       {})
    nedt = manifest.get("NEdT",        {})
    print(f"  coefficients   : {'YES' if cal.get('has_coefficients')   else 'no'}")
    print(f"  image_stack    : {'YES' if cal.get('has_image_stack')    else 'no'}")
    print(f"  stability_data : {'YES' if stab.get('has_stability_data') else 'no'}")
    print(f"  NEdT data      : {'YES' if nedt.get('coefficients_used')   else 'no'}")
    print(f"  rsr            : {cal.get('rsr_type', 'none')}")
    print(f"  cal directory  : {cal.get('directory', 'n/a')}")
    print(f"  current image  : {img.get('current_image_path') or '(none — directory was selected)'}")
    if arrays:
        print(f"  --- arrays.npz ---")
        for k, v in arrays.items():
            print(f"    [{k}]  shape={v.shape}  dtype={v.dtype}  {v.nbytes/1e6:.1f} MB")


# ══════════════════════════════════════════════════════════════════════════════
#  LOAD
# ══════════════════════════════════════════════════════════════════════════════

def load_project(main_window, folder_path: str) -> None:
    import LWIRImageTool as lit
    from core.image_display import prepare_for_qt
    from PySide6.QtWidgets  import QTreeWidgetItem
    from PySide6.QtCore     import Qt
    from PySide6.QtGui      import QPixmap

    manifest_path = os.path.join(folder_path, MANIFEST_FILENAME)
    arrays_path   = os.path.join(folder_path, ARRAYS_FILENAME)

    if not os.path.isfile(manifest_path):
        raise FileNotFoundError(f"No project.json found in: {folder_path}")

    print(f"\n[ProjectSerializer] Loading ← {folder_path}")

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    schema = manifest.get("schema_version", "unknown")
    if schema != PROJECT_SCHEMA_VERSION:
        print(f"[ProjectSerializer] Warning: schema mismatch "
              f"(file={schema}, app={PROJECT_SCHEMA_VERSION}). Attempting load anyway.")

    npz = {}
    if os.path.isfile(arrays_path):
        loaded = np.load(arrays_path)
        npz    = {k: loaded[k] for k in loaded.files}
        print(f"[ProjectSerializer] arrays.npz keys: {list(npz.keys())}")
    else:
        print(f"[ProjectSerializer] No arrays.npz found — skipping array restore.")

    mw = main_window

    # ── 1. File lists & navigation ────────────────────────────────────────────
    print("[ProjectSerializer] Restoring file lists...")
    try:
        files                = manifest.get("files", {})
        mw.list_of_files     = files.get("list_of_files",     [])
        mw.item_selected     = files.get("item_selected",     "")
        mw.index             = files.get("current_index",     0)
        mw.list_of_valid_files = files.get("list_of_valid_files", [])

        mw.filesRoot.takeChildren()
        added_dirs = set()
        for path in mw.list_of_files:
            if path and path not in added_dirs and os.path.isdir(path):
                mw.AddDirectoryToTree(path)
                added_dirs.add(path)
            elif path and os.path.isfile(path):
                mw.AddFileToTree(path)

        print(f"[ProjectSerializer]   item_selected : {mw.item_selected}")
        print(f"[ProjectSerializer]   current_index : {mw.index}")
        print(f"[ProjectSerializer]   dir_files     : {len(mw.list_of_valid_files)} entries")
    except Exception:
        print("[ProjectSerializer] ERROR restoring file lists:")
        traceback.print_exc()

    # ── 2. Calibration data ───────────────────────────────────────────────────
    print("[ProjectSerializer] Restoring calibration data...")
    try:
        cal_manifest = manifest.get("calibration", {})
        if cal_manifest.get("has_coefficients") or cal_manifest.get("has_image_stack"):
            restored            = _RestoredCalibrationData(cal_manifest, npz)
            mw.calibration_data = restored

            label = (os.path.basename(cal_manifest.get("directory") or "")
                     or "calibration_data")
            var_item = QTreeWidgetItem(mw.varsRoot)
            var_item.setText(0, label + "_cal_coefficients")
            var_item.setData(0, Qt.UserRole, restored)

            print(f"[ProjectSerializer]   coefficients : "
                  f"{restored.coefficients.shape if restored.coefficients is not None else 'None'}")
            print(f"[ProjectSerializer]   image_stack  : "
                  f"{restored.image_stack.shape  if restored.image_stack  is not None else 'None'}")
        else:
            print("[ProjectSerializer]   No calibration data in project file.")
    except Exception:
        print("[ProjectSerializer] ERROR restoring calibration data:")
        traceback.print_exc()

    # ── 3. NEdT data ───────────────────────────────────────────────────
    print("[ProjectSerializer] Restoring NEdT data...")
    try:
        NEdT_manifest = manifest.get("NEdT", {})
        if NEdT_manifest.get("coefficients_used") and "NEdT_Data" in npz:
            mw.NEdT_Data = npz["NEdT_Data"]

            label = (os.path.basename(NEdT_manifest.get("directory")))
            var_item = QTreeWidgetItem(mw.varsRoot)
            var_item.setText(0, label + "_NEdT_array")
            var_item.setData(0, Qt.UserRole, mw.NEdT_Data)

            print(f"[ProjectSerializer]   NEdT Array : "
                  f"{mw.NEdT_Data.shape if mw.NEdT_Data is not None else 'None'}")
        else:
            print("[ProjectSerializer]   No NEdT data in project file.")
    except Exception:
        print("[ProjectSerializer] ERROR restoring NEdT data:")
        traceback.print_exc()

    # ── 4. Stability data ─────────────────────────────────────────────────────
    print("[ProjectSerializer] Restoring stability data...")
    try:
        if manifest.get("stability", {}).get("has_stability_data") and "stability_data" in npz:
            mw.stability_data = npz["stability_data"]
            var_item = QTreeWidgetItem(mw.varsRoot)
            var_item.setText(0, manifest.get("stability", {}).get("stability_var_name"))
            var_item.setData(0, Qt.UserRole, mw.stability_data)
            print(f"[ProjectSerializer]   shape: {mw.stability_data.shape}")
        else:
            print("[ProjectSerializer]   No stability data in project file.")
    except Exception:
        print("[ProjectSerializer] ERROR restoring stability data:")
        traceback.print_exc()

    # ── 5. Current image ──────────────────────────────────────────────────────
    print("[ProjectSerializer] Restoring current image...")
    try:
        img_path = manifest.get("image", {}).get("current_image_path", "")
        if img_path and os.path.isfile(img_path):
            factory          = lit.ImageDataFactory()
            config           = lit.ImageDataConfig(filename=img_path, fileformat="rjpeg")
            if factory.is_valid_image_file(img_path, "rjpeg"):
                mw.current_image = factory.create_from_file(config)
                qimg             = prepare_for_qt(mw.current_image.raw_counts)
                mw.ui.imagelabel.setPixmap(QPixmap.fromImage(qimg))
                print(f"[ProjectSerializer]   Loaded: {img_path}")
            else:
                print(f"[ProjectSerializer]   Invalid image file, skipping: {img_path}")
        elif img_path:
            print(f"[ProjectSerializer]   File not found on disk, skipping: {img_path}")
        else:
            print(f"[ProjectSerializer]   No image path saved (directory was selected at save time).")
    except Exception:
        print("[ProjectSerializer] ERROR restoring current image:")
        traceback.print_exc()

    # ── 6. UI state ───────────────────────────────────────────────────────────
    print("[ProjectSerializer] Restoring UI state...")
    try:
        mw.loading_project = True
        ui      = manifest.get("ui", {})
        tab_map = {
            "imageTab":     mw.ui.imageTab,
            "calTab":       mw.ui.calTab,
            "nedtTab":      mw.ui.nedtTab,
            "stabilityTab": mw.ui.stabilityTab,
        }
        for tab_name, enabled in ui.get("tab_enabled", {}).items():
            if tab_name in tab_map:
                mw.ui.tabWidget.setTabEnabled(
                    mw.ui.tabWidget.indexOf(tab_map[tab_name]), enabled)

        mw.ui.frameSelection.setValue(ui.get("frame_slider_value", 0))
        mw.ui.rowTextEdit.setPlainText(ui.get("row_text", "0"))
        mw.ui.colTextEdit.setPlainText(ui.get("col_text", "0"))

        # Set active tab last to avoid spurious OnTabChanged triggers
        mw.ui.tabWidget.setCurrentIndex(ui.get("active_tab_index", 0))
        print(f"[ProjectSerializer]   Active tab: {ui.get('active_tab_index', 0)}")

        # Plot all existing variables to save user from re-running computations
        if mw.calibration_data is not None:
            pixel_stats = prepare_pixel(mw.calibration_data, 0, 0)
            mw.ViewCalibrationInfo(pixel_stats)
        if mw.NEdT_Data is not None and mw.calibration_data is not None:
            mw.temps = mw.calibration_data.blackbody_temperature + mw.calibration_data.temperature_step * np.arange(mw.calibration_data._number_of_steps)
            mw.median_NEDT  = np.percentile(mw.NEdT_Data, 50,  axis=(0,1))  # same as median
            mw.ViewNEDTInfo(mw.NEdT_Data[0,0,:], mw.temps)
        if mw.stability_data is not None:
            ax = mw.stabilityCanvas.get_single_grid()
            ax.plot(mw.stability_data)
            ax.set_title("Mean pixel value across frames")
            ax.set_xlabel("Frame number")
            ax.set_ylabel("Mean Digital Count")
            mw.stabilityCanvas.draw()

    except Exception:
        print("[ProjectSerializer] ERROR restoring UI state:")
        traceback.print_exc()

    print(f"[ProjectSerializer] Load complete.\n")


# ══════════════════════════════════════════════════════════════════════════════
#  Restored CalibrationData container
# ══════════════════════════════════════════════════════════════════════════════

class _RestoredCalibrationData:
    """
    Stand-in for LWIRImageTool.BlackbodyCalibration.
    Holds numpy arrays and metadata. Exposes find_ascensions() so
    pixel_stats.py works without modifications or a re-run.
    """

    def __init__(self, cal_manifest: dict, npz: dict):
        self.coefficients = npz.get("coefficients", None)  # (rows, cols, 2)
        self.image_stack  = npz.get("image_stack",  None)  # (rows, cols, frames)

        rsr_type = cal_manifest.get("rsr_type", "none")
        if rsr_type == "ndarray":
            self.rsr = npz.get("rsr", None)
        elif rsr_type == "path":
            self.rsr = cal_manifest.get("rsr_path", None)
        else:
            self.rsr = None

        self.directory             = cal_manifest.get("directory",             "")
        self.filetype              = cal_manifest.get("filetype",              "rjpeg")
        self.blackbody_temperature = cal_manifest.get("blackbody_temperature", None)
        self.temperature_step      = cal_manifest.get("temperature_step",      None)
        self.environmental_temperature = cal_manifest.get("environmenttal_temperature", None)
        self.deriv_threshold       = cal_manifest.get("deriv_threshold",       3.0)
        self.window_fraction       = cal_manifest.get("window_fraction",       0.001)
        self._number_of_steps      = cal_manifest.get("_number_of_steps", None)
        self._array_of_avg_coords = cal_manifest.get("_array_of_avg_coords", None)

