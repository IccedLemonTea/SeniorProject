# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connecting open image tab to trigger
        self.ui.actionOpenImage.triggered.connect(self.open_image)
        # Connecting Open Directory to trigger
        self.ui.actionOpenBBDirectory.triggered.connect(self.open_blackbody_directory)

        self.ui.actionPerformCalibration.triggered.connect(self.blackbody_calbration)

    # Open a directory of images and store them within the GUI's memory
    # Input : self
    # Action : Asks user ro select a dir path, then loads in all imagery within that dir.
    def open_blackbody_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            ""
            )

        if not directory:
            return  # User cancelled

        QMessageBox.information(
            self,
            "Directory Selected",
            f"You selected:\n{directory}"
            )

    # Open a singular image to view
    # Input : self
    # Action : Changes the main window and dispays the image that is selected.
    def open_image(self):
        print("Hello World!")

    # Performs the blackbody calibration and relates DC to Radiance at each pixel.
    #



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
