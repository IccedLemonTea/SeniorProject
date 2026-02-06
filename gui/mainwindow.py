# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidget, QListWidgetItem, QLabel, QTreeWidgetItem
from PySide6.QtCore import QObject, Signal, Qt, QThread
import LWIRImageTool as lit
from core.Workers import CalibrationWorker
from core.image_display import prepare_for_qt
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

        # Disable tabs
        for tab in [self.ui.imageTab, self.ui.calTab, self.ui.nedtTab, self.ui.stabilityTab]:
            self.ui.tabWidget.setTabEnabled(
                self.ui.tabWidget.indexOf(tab), False
            )

        # Force default tab (Image Preview)
        self.ui.tabWidget.setCurrentIndex(
            self.ui.tabWidget.indexOf(self.ui.imageTab)
        )   

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

        self.ui.tabWidget.currentChanged.connect(self.OnTabChanged)

        self.ui.widgetProjectTreeList.itemClicked.connect(self.OnTreeClicked)

        self.ui.frameSelection.valueChanged.connect(self.OnFrameChanged)

        self.filesRoot = self.ui.widgetProjectTreeList.topLevelItem(0)
        self.varsRoot  = self.ui.widgetProjectTreeList.topLevelItem(1)


    def AddDirectoryToTree(self, directory):
        root = QTreeWidgetItem(self.filesRoot)
        root.setText(0, os.path.basename(directory))
        root.setData(0, Qt.UserRole, directory)

        for fname in sorted(os.listdir(directory)):
            child = QTreeWidgetItem(root)
            child.setText(0, fname)
            child.setData(0, Qt.UserRole, os.path.join(directory, fname))

        root.setExpanded(False)

    def OnFrameChanged(self, index):
        if not hasattr(self, "current_dir_files"):
            return

        if 0 <= index < len(self.current_dir_files):
            self.item_selected = self.current_dir_files[index]
            self.ViewImage()

    def OnTabChanged(self, index):
        """Triggered when tab is switched"""

        tab_text = self.ui.tabWidget.tabText(index)
        # Act based on index or label
        if index == 0:
            self.ViewImage()
        elif index == 1:
            self.Calibration()

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
        self.list_of_files.append(filepath)
        list_item = QListWidgetItem()
        list_item.setData(0,filepath)
        self.ui.widgetProjectFileList.addItem(list_item)
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
            
            self.list_of_files.append(directory)
            self.AddDirectoryToTree(directory)
            self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.indexOf(self.ui.calTab), True)
            self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.indexOf(self.ui.stabilityTab), True)

            self.current_dir_files = sorted([
            os.path.join(directory, f)
            for f in os.listdir(directory)
            ])

            num_files = len(self.current_dir_files)
            self.ui.frameSelection.setMinimum(0)
            self.ui.frameSelection.setMaximum(max(0, num_files - 1))

    def OnTreeClicked(self, item, column):
        data = item.data(0, Qt.UserRole)

        if isinstance(data, str) and os.path.isfile(data):
            # disk file
            self.item_selected = data
            self.ViewImage()

        elif isinstance(data, lit.ImageData):   # your image class
            # in-memory image
            qimg = prepare_for_qt(data.raw_counts)
            self.ui.imagelabel.setPixmap(QPixmap.fromImage(qimg))

    def ViewImage(self, frame=None):
        if not self.item_selected:
            return

        Factory = lit.ImageDataFactory()
        config = lit.ImageDataConfig(
            filename=self.item_selected,
            fileformat="rjpeg"
        )

        image = Factory.create_from_file(config)

        qimg = prepare_for_qt(image.raw_counts)
        pixmap = QPixmap.fromImage(qimg)

        self.ui.imagelabel.setPixmap(pixmap)

        # Add to Variables section
        var_item = QTreeWidgetItem(self.varsRoot)
        var_item.setText(0, os.path.basename(self.item_selected))

        # Store the ACTUAL image object
        var_item.setData(0, Qt.UserRole, image)
        self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.indexOf(self.ui.imageTab), True)

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
