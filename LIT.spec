# ============================================================
#  LIT.spec    PyInstaller build configuration
#  Longwave Infrared Tool (LIT)
#
#  Usage:
#      pyinstaller SeniorProject/LIT.spec
#
#  Run from the root of your project, e.g.:
#      ~/Desktop/Senior_Project_Test/
#
#  Output:
#      dist/LIT/          (onedir build  recommended)
# ============================================================

import sys
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_all

# -- Path helpers ---------------------------------------------
block_cipher = None

# Detect platform and set the path to LWIRImageTool source accordingly.
#
#   Linux / macOS:
#       ~/Desktop/LWIRImageTool/LWIRImageTool/
#
#   Windows  update WINDOWS_LIT_ROOT to wherever you cloned LWIRImageTool.
#
WINDOWS_LIT_ROOT = r"C:\Users\Cooper\OneDrive - rit.edu\Desktop\Senior Project\sUAS Docs\Code\LWIRImageTool"
UNIX_LIT_ROOT    = str(Path.home() / "Desktop" / "LWIRImageTool")

if sys.platform == "win32":
    LWIR_ROOT = WINDOWS_LIT_ROOT
else:
    LWIR_ROOT = UNIX_LIT_ROOT

# The actual package source folder (contains __init__.py)
LWIR_PKG = str(Path(LWIR_ROOT) / "LWIRImageTool")

# Sanity check  fail loudly at build time if the path is wrong
if not Path(LWIR_PKG).is_dir():
    raise FileNotFoundError(
        f"LWIRImageTool package not found at: {LWIR_PKG}\n"
        f"Update WINDOWS_LIT_ROOT or UNIX_LIT_ROOT in LIT.spec to match "
        f"where LWIRImageTool is cloned on this machine."
    )

# -- Collect scipy (fixes broken extension module bundling) ---
datas_scipy, binaries_scipy, hiddenimports_scipy = collect_all('scipy')

# -- Hidden imports -------------------------------------------
hidden_imports = [
    # PySide6 modules used at runtime
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',

    # Matplotlib backend that PySide6 uses
    'matplotlib.backends.backend_qt5agg',

    # Your core subpackage
    'core.Workers',
    'core.image_display',
    'core.plot_canvas',
    'core.pixel_stats',
    'core.calibration_dialog',
    'core.project_serializer',
    'core.select_RSR',

    # Your gui subpackage
    'gui.ui_form',

    # LWIRImageTool modules
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

    # pydantic
    'pydantic',
    'pydantic.v1',

    # Other dependencies
    'scipy',
    'scipy.integrate',
    'scipy.constants',
    'spectral',
    'spectral.io.envi',
    'PIL',
    'PIL.Image',

    # scipy compiled extension modules that PyInstaller misses
    'scipy._cyutility',
    'scipy._lib._ccallback_c',
    'scipy._lib.messagestream',
]

# Collect submodules automatically
hidden_imports += collect_submodules('pydantic')
hidden_imports += collect_submodules('matplotlib')
hidden_imports += collect_submodules('numpy')

# Wire in the scipy hidden imports collected by collect_all
hidden_imports += hiddenimports_scipy

# -- Data files -----------------------------------------------
datas = [
    # LWIRImageTool package source
    (LWIR_PKG, 'LWIRImageTool'),

    # Your core and gui packages  PyInstaller needs these copied in explicitly
    ('core', 'core'),
    ('gui', 'gui'),

    # Matplotlib fonts, style sheets, etc.
    *collect_data_files('matplotlib'),

    # scipy data files (collected by collect_all above)
    *datas_scipy,
]

# -- Binaries -------------------------------------------------
binaries = [
    # scipy compiled .so/.pyd extension modules (collected by collect_all above)
    *binaries_scipy,
]

# -- Analysis -------------------------------------------------
a = Analysis(
    ['gui/mainwindow.py'],
    pathex=[
        '.',                    # Root of your project (Senior_Project_Test/)
        'SeniorProject',        # Where core/ and gui/ live
        LWIR_ROOT,              # LWIRImageTool root (cross-platform)
    ],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# -- PYZ archive ----------------------------------------------
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
    exclude_binaries=True,
    name='LIT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,               # Keep True while debugging  flip to False for release
    # icon='gui/icons/lit_icon.ico',
)

# -- COLLECT --------------------------------------------------
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LIT',
)
