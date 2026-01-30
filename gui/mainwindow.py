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

        # self.ui.tabWidget.currentChanged.connect(self.OnTabChanged)

        self.ui.widgetWorkspaceList.itemClicked.connect(self.OnItemClicked)

        # Disable tabs
        for tab in [self.ui.imageTab, self.ui.calTab, self.ui.nedtTab, self.ui.stabilityTab]:
            self.ui.tabWidget.setTabEnabled(
                self.ui.tabWidget.indexOf(tab), False
            )

        # Force default tab (Image Preview)
        self.ui.tabWidget.setCurrentIndex(
            self.ui.tabWidget.indexOf(self.ui.imageTab)
        )



    # def OnTabChanged(self, index):
    #     """Triggered when tab is switched"""

    #     tab_text = self.ui.tabWidget.tabText(index)
    #     # Act based on index or label
    #     if index == 0:
    #         # self.ViewImage()
    #     elif index == 1:
    #         # self.Calibration()

    # TODO
    def Calibration(self):
        self.StartCalibration(self.item_selected, filetype = 'rjpeg', rsr=None)
    
    def OpenImage(self):
        filepath,_ = QFileDialog.getOpenFileName(
            self,
            "Select RSR file path",
            "","All Files (*)"
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
        # relative_path = os.path.relpath(filepath[0], self.home_dir)
        self.list_of_files.append(filepath[0])
        list_item = QListWidgetItem()
        list_item.setData(0,filepath[0])
        self.ui.widgetWorkspaceList.addItem(list_item)
        self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.indexOf(self.ui.imageTab), True)
    
    def OpenRSRText(self):
        rsr_path,_ = QFileDialog.getOpenFileName(
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
        directory,_ = QFileDialog.getExistingDirectory(
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
            self.list_of_files.append(directory)
            list_item = QListWidgetItem()
            list_item.setData(0,directory)
            self.ui.widgetWorkspaceList.addItem(list_item)
            self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.indexOf(self.ui.calTab), True)
            self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.indexOf(self.ui.stabilityTab), True)

    def OnItemClicked(self,item):
        self.item_selected = item.text()

    def ViewImage(self):
        Factory = lit.ImageDataFactory()
        config = lit.ImageDataConfig(filename = self.item_selected, fileformat = "rjpeg")
        image = Factory.create_from_file(config)

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

    def StartCalibration(self, directory, filetype, rsr=None):
        self.thread = QThread()
        self.worker = CalibrationWorker(directory, filetype, rsr)

        self.worker.moveToThread(self.thread)

        # Wiring
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.UpdateProgress)
        self.worker.finished.connect(self.CalibrationFinished)


        # Cleanup
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # UI state
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setFormat("Starting calibration...")

        self.thread.start()

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
        self.tabWidget.setTabEnabled(self.tabWidget.indexOf(self.nedtTab), True)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
