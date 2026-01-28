# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidget, QListWidgetItem, QLabel
from PySide6.QtCore import QObject, Signal, QThread
import LWIRImageTool as lit
from workers.CalibrationWorker import CalibrationWorker
import numpy as np

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from gui.ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        ### GUI Wide Variables ###
        self.list_of_files = []
        self.item_selected = ""


        # Necessary for ease of access, limits the amount of text in the file list
        self.home_dir = os.path.expanduser("~")

        # Connecting actions to triggers
        self.ui.actionOpenImage.triggered.connect(self.OpenImage)
        self.ui.actionOpenBBDirectory.triggered.connect(self.OpenBlackbodyDirectory)
        # self.ui.actionOpen_Other.triggered.connect(self.open_other) # TODO

        self.ui.actionChooseCalibration.triggered.connect(self.Calibration)

        # self.ui.actionView_Selected_Image.triggered.connect(self.ViewImage)


        self.ui.widgetWorkspaceList.itemClicked.connect(self.OnItemClicked)

    # TODO
    def Calibration(self):
        print("Hello World!")

        self.StartCalibration(directory, filetype = 'rjpeg', rsr=None)

    def OpenRSRText(self):
        rsr_path = QFileDialog.getOpenFileName(
        self,
        "Select RSR file path",
        "","*.txt;;All Files (*)"
        )

        if not rsr_path:
            return 
        else:
            QMessageBox.information(
                self,
                "RSR Selected",
                f"You selected:\n{rsr_path}"
                )
            self.list_of_files.append(rsr_path)
        
            
    def OpenBlackbodyDirectory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            ""
            )

        if not directory:
            QMessageBox.information(
            self,
            "No Directory Selected"
            )
            return
        else:
            QMessageBox.information(
                self,
                "Directory Selected",
                f"You selected:\n{directory}"
                )
            
            relative_path = os.path.relpath(directory, self.home_dir)
            self.list_of_files.append(relative_path)
            list_item = QListWidgetItem()
            list_item.setData(0,relative_path)
            self.ui.widgetWorkspaceList.addItem(list_item)


            
        
    def OnItemClicked(self,item):
        self.item_selected = item.text()
        
    # TODO
    def OpenImage(self):
        filepath = QFileDialog.getOpenFileName(
            self,
            "Select RSR file path",
            "","*.txt;;All Files (*)"
        )

        if not filepath:
            QMessageBox.information(
            self,
            "No File Selected"
            )
            return
        else:
            QMessageBox.information(
                self,
                "File Selected",
                f"You selected:\n{filepath}"
                )
        print(f"the filetype is {filepath[0]} and the type is {type(filepath[0])}")
        relative_path = os.path.relpath(filepath[0], self.home_dir)
        self.list_of_files.append(relative_path)
        list_item = QListWidgetItem()
        list_item.setData(0,relative_path)
        self.ui.widgetWorkspaceList.addItem(list_item)

        Factory = lit.ImageDataFactory()
        image = Factory.create_from_file(filepath[0],"rjpeg")

        arr = image.raw_counts

        arr_disp = arr.astype(np.float32)
        arr_disp -= arr_disp.min()
        arr_disp /= arr_disp.max()
        arr_disp *= 65535
        arr_disp = arr_disp.astype(np.uint16)


        h, w = arr.shape
        bytes_per_line = w*2

        q_image = QImage(
            arr_disp.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_Grayscale16
        )

        pixmap = QPixmap.fromImage(q_image)
        self.ui.imagelabel.setPixmap(pixmap)
        self.list_of_files.append(filepath[0])


    def UpdateProgress(self, phase, current, total):
        percent = int((current / total) * 100)

        if phase == "loading":
            self.ui.progressBar.setFormat("Loading images... %p%")
        elif phase == "calibrating":
            self.ui.progressBar.setFormat("Calibrating pixels... %p%")
        elif phase == "ascension":
            self.ui.progressBar.setFormat("Calculating ascension regions... %p%")

        self.ui.progressBar.setValue(percent)

    def CalibrationFinished(self, cal_array):
        self.ui.progressBar.setValue(100)
        self.ui.progressBar.setFormat("Calibration complete")

        self.calibration_data = cal_array

        QMessageBox.information(
            self,
            "Calibration Finished",
            "Blackbody calibration completed successfully."
        )
        print(f"{self.calibration_data}")

    def StartCalibration(self, directory, filetype, rsr=None):
        self.thread = QThread()
        self.worker = CalibrationWorker(directory, filetype, rsr)

        self.worker.moveToThread(self.thread)

        # Wiring
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.calibration_finished)


        # Cleanup
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # UI state
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setFormat("Starting calibration...")

        self.thread.start()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
