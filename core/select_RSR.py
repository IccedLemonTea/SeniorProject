import os
from PySide6.QtWidgets import QMessageBox, QInputDialog  # fixed casing
from PySide6.QtCore import Qt


def select_rsr(files_root, parent) -> str | None:
    """
    Scans the files_root QTreeWidgetItem for .txt files and prompts
    the user to pick one. Returns the selected path, or None on failure/cancel.
    """
    rsr_files = []
    for i in range(files_root.childCount()):
        child = files_root.child(i)
        data = child.data(0, Qt.UserRole)
        if isinstance(data, str) and os.path.isfile(data) and data.endswith('.txt'):
            rsr_files.append((child.text(0), data))

    if not rsr_files:
        QMessageBox.critical(
            parent,
            "No RSR Files",
            "No .txt files found in Project Files. Please load an RSR file first."
        )
        return None

    if len(rsr_files) == 1:
        QMessageBox.information(
            parent,
            "RSR File Selected",
            f"Using RSR file:\n{rsr_files[0][0]}"
        )
        return rsr_files[0][1]

    # Multiple files — let the user pick
    items = [name for name, path in rsr_files]
    item, ok = QInputDialog.getItem(
        parent,
        "Select RSR File",
        "Multiple .txt files found. Select the RSR file to use:",
        items, 0, False
    )
    if not ok:
        return None

    return next(path for name, path in rsr_files if name == item)