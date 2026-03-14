# ============================================================
#  LIT.spec    PyInstaller build configuration
#  Longwave Infrared Tool (LIT)
#
#  Usage:
#      pyinstaller LIT.spec
#
#  Output:
#      dist/LIT/          (onedir build  recommended)
#
#  Notes:
#    - Run this from the root of your project directory, i.e.
#      the folder that contains mainwindow.py, core/, and gui/
#    - If LWIRImageTool is a compiled extension (.pyd / .so),
#      see the BINARIES section below
# ============================================================

import sys
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# -- Path helpers ---------------------------------------------
block_cipher = None   # Set to a Cipher object if you want to encrypt bytecode

# Detect platform and set the path to LWIRImageTool source accordingly.
#
# LWIRImageTool lives in a directory parallel to Senior_Project:
#
#   Linux / macOS:
#       ~/Desktop/LWIRImageTool/LWIRImageTool/
#
#   Windows  update WINDOWS_LIT_ROOT to wherever you cloned LWIRImageTool.
#   e.g. r"C:\Users\cjw9009\Desktop\LWIRImageTool"
#
WINDOWS_LIT_ROOT = r"C:\Users\Cooper\OneDrive - rit.edu\Desktop\Senior Project\sUAS Docs\Code\LWIRImageTool"
UNIX_LIT_ROOT    = str(Path.home() / "Desktop" / "LWIRImageTool")

if sys.platform == "win32":
    LWIR_ROOT    = WINDOWS_LIT_ROOT
else:
    LWIR_ROOT    = UNIX_LIT_ROOT

# The actual package source folder (contains __init__.py)
LWIR_PKG = str(Path(LWIR_ROOT) / "LWIRImageTool")

# Sanity check  fail loudly at build time if the path is wrong
if not Path(LWIR_PKG).is_dir():
    raise FileNotFoundError(
        f"LWIRImageTool package not found at: {LWIR_PKG}\n"
        f"Update WINDOWS_LIT_ROOT or UNIX_LIT_ROOT in LIT.spec to match "
        f"where LWIRImageTool is cloned on this machine."
    )


# -- Hidden imports -------------------------------------------
# PyInstaller's static analysis sometimes misses dynamically-loaded
# submodules. List any that cause "ModuleNotFoundError" at runtime here.
hidden_imports = [
    # PySide6 modules used at runtime
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',

    # Matplotlib backend that PySide6 uses
    'matplotlib.backends.backend_qt5agg',

    # Your core subpackage  add any modules PyInstaller misses
    'core.Workers',
    'core.image_display',
    'core.plot_canvas',
    'core.pixel_stats',
    'core.calibration_dialog',
    'core.project_serializer',
    'core.select_RSR',

    # Your gui subpackage
    'gui.ui_form',

    # LWIRImageTool is pure Python  all classes re-exported via __init__.py
    # using relative imports. List each module file explicitly so PyInstaller
    # traces them. Do NOT use collect_submodules() here  the submodules are
    # not independently importable as e.g. 'LWIRImageTool.Blackbody' from
    # outside the package; PyInstaller needs them listed to find the .py files.
    'LWIRImageTool',
    'LWIRImageTool.Blackbody',
    'LWIRImageTool.BlackbodyCalibration',
    'LWIRImageTool.BlackbodyCalibrationConfig',
    'LWIRImageTool.CalibrationData',
    'LWIRImageTool.CalibrationDataFactory',
    'LWIRImageTool.ENVI',
    'LWIRImageTool.ImageData',
    'LWIRImageTool.ImageDataConfig',
    'LWIRImageTool.ImageDataFactory',
    'LWIRImageTool.NEDT',
    'LWIRImageTool.RJPEG',
    'LWIRImageTool.SFMOV',
    'LWIRImageTool.StackImages',

    # pydantic is used heavily by LWIRImageTool and uses dynamic imports
    'pydantic',
    'pydantic.v1',

    # Other LWIRImageTool dependencies
    'scipy',
    'scipy.integrate',
    'scipy.constants',
    'spectral',
    'spectral.io.envi',
    'PIL',
    'PIL.Image',
]

# Automatically collect submodules  collect_submodules('LWIRImageTool')
# intentionally removed; see comment above
hidden_imports += collect_submodules('pydantic')
hidden_imports += collect_submodules('matplotlib')
hidden_imports += collect_submodules('numpy')


# -- Data files -----------------------------------------------
# Tuple format: ('source path on your machine', 'destination folder in bundle')
#
# Add any non-Python files your app reads at runtime:
#   - RSR .txt files bundled as defaults
#   - Qt .ui files if you load them at runtime instead of using ui_form.py
#   - Icons, images, config files, etc.
#
datas = [
    # Explicitly copy the entire LWIRImageTool package into the bundle.
    # This is necessary because pip install -e creates a pointer file rather
    # than copying sources into site-packages, so PyInstaller needs to be
    # told where the actual .py files live.
    (LWIR_PKG, 'LWIRImageTool'),  # cross-platform  path resolved above

    # Example: bundle a default RSR file into a 'data' subfolder in the exe
    # ('path/to/your/default_rsr.txt', 'data'),

    # Example: bundle the Qt .ui file if needed at runtime
    # ('gui/form.ui', 'gui'),

    # Collect all data files from matplotlib (fonts, style sheets, etc.)
    *collect_data_files('matplotlib'),
]


# -- Binaries -------------------------------------------------
# If LWIRImageTool is a compiled C extension (.pyd on Windows, .so on Linux/mac)
# rather than pure Python, add it here so PyInstaller copies it into the bundle.
#
# Format: ('path/to/extension.pyd', 'destination subfolder in bundle')
#
binaries = [
    # ('path/to/LWIRImageTool.cp311-win_amd64.pyd', '.'),   # Windows example
    # ('path/to/LWIRImageTool.cpython-311-x86_64.so', '.'), # Linux example
]



# -- Analysis -------------------------------------------------
# This is the core step  PyInstaller traces all imports starting
# from your entry point (mainwindow.py) and builds the dependency graph.
a = Analysis(
    ['gui/mainwindow.py'],      # Entry point your main script
    pathex=[
        '.',                    # Root of your project
        LWIR_ROOT,              # LWIRImageTool source cross-platform path
    ],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],               # Custom hooks folder if you have one
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Packages you know are NOT needed  keeps the bundle smaller
        # NOTE: do NOT exclude standard library modules like 'email',
        # 'html', 'http', 'xmlrpc', or 'unittest'  pydantic, matplotlib,
        # and pyparsing all depend on them transitively at import time.
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# -- PYZ archive ----------------------------------------------
# Compresses all collected .pyc bytecode into a single archive
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

# -- EXE ------------------------------------------------------
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,      # True = onedir mode (recommended)
                                # False = onefile mode (slower startup)
    name='LIT',                 # Name of the output executable
    debug=False,                # Set True to get verbose runtime output
                                # while troubleshooting missing imports
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                   # Compress binaries with UPX if installed
                                # (reduces folder size, optional)
    console=False,              # False = no terminal window (GUI app)
                                # Set True temporarily if you need to see
                                # print/error output while debugging
    # icon='gui/icons/lit_icon.ico',  # Uncomment and set path to your icon
)

# -- COLLECT --------------------------------------------------
# Gathers the exe, all binaries, zipfiles, and datas into the
# final output folder:  dist/LIT/
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LIT',                 # Output folder name inside dist/
)
