# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidget, QListWidgetItem, QLabel, QTreeWidgetItem
from PySide6.QtCore import QObject, Signal, Qt, QThread
import LWIRImageTool as lit
from core.Workers import CalibrationWorker
from core.image_display import prepare_for_qt
from core.plot_canvas import MplCanvas
from core.pixel_stats import prepare_pixel
from core.calibration_dialog import CalibrationDialog
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
        # Making sure pop ups follow Palette
        QApplication.instance().setPalette(self.palette())


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
        self.current_image = None
        self.active_calibration = False
        self.index = 0

        # ---- Matplotlib canvas inside calibration tab ----
        self.calCanvas = MplCanvas(self.ui.calibrationPlotContainer)
        self.ui.calPlotLayout.addWidget(self.calCanvas)



        # Necessary for ease of access, limits the amount of text in the file list
        self.home_dir = os.path.expanduser("~")

        # Connecting actions to triggers
        self.ui.actionOpenImage.triggered.connect(self.OpenImage)
        self.ui.actionOpenBBDirectory.triggered.connect(self.OpenBlackbodyDirectory)
        # self.ui.actionOpen_Other.triggered.connect(self.open_other) # TODO
        
        # Connecting actions to buttons and tabs
        self.ui.actionChooseCalibration.triggered.connect(self.Calibration)
        self.ui.tabWidget.currentChanged.connect(self.OnTabChanged)
        self.ui.widgetProjectTreeList.itemClicked.connect(self.OnTreeClicked)
        self.ui.frameSelection.valueChanged.connect(self.OnFrameChanged)
        self.filesRoot = self.ui.widgetProjectTreeList.topLevelItem(0)
        self.varsRoot  = self.ui.widgetProjectTreeList.topLevelItem(1)
        self.ui.saveImage.clicked.connect(self.SaveImage)
        self.ui.nextFrame.clicked.connect(self.NextFrame)
        self.ui.priorFrame.clicked.connect(self.PriorFrame)

    def NextFrame(self):
        max_index = len(self.current_dir_files)
        if self.index < max_index:
            self.index = self.index + 1
            self.ui.frameSelection.setValue(self.index)
              
    def PriorFrame(self):

        if self.index > 0:
            self.index = self.index -1
            self.ui.frameSelection.setValue(self.index)
            
    def AddDirectoryToTree(self, directory):
        root = QTreeWidgetItem(self.filesRoot)
        root.setText(0, os.path.basename(directory))
        root.setData(0, Qt.UserRole, directory)

        for fname in sorted(os.listdir(directory)):
            child = QTreeWidgetItem(root)
            child.setText(0, fname)
            child.setData(0, Qt.UserRole, os.path.join(directory, fname))

        root.setExpanded(False)

    def OnFrameChanged(self):
        if 0 <= self.index < len(self.current_dir_files):
            self.item_selected = self.current_dir_files[self.index]
            self.ViewImage()

    def OnTabChanged(self, index):
        """Triggered when tab is switched"""

        tab_text = self.ui.tabWidget.tabText(index)
        # Act based on index or label
        if index == 0:
            self.ViewImage()
        elif index == 1:
            self.Calibration()

    def Calibration(self):
        if not self.active_calibration:
            reply = QMessageBox.question(
                self,
                "Calibration",
                "Do you want to perform a calibration run?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.No:
                return   # user chickened out

            # ---- Open advanced dialog ----
            dlg = CalibrationDialog(self)

            if dlg.exec():   # User pressed Start
                settings = dlg.getValues()

                if settings["use_rsr"]:
                    self.StartCalibration(self.item_selected, "rjpeg")
                else:
                    fwhm_width = float(settings["fwhm_width"])
                    fwhm_center = float(settings["fwhm_center"])
                    num_samples = int(settings["num_samples"])

                    ### Generating Rect FWHM for simulated RSR ###
                    wavelengths = np.linspace(fwhm_center-fwhm_width/2.0, fwhm_center+fwhm_width/2.0, num_samples)
                    response = np.ones(shape=[num_samples], dtype=float)
                    response[0] = 0.5
                    response[response.shape[0]-1] = 0.5
                    rsr_sim = np.array([wavelengths, response])

                    print(rsr_sim)

                    self.StartCalibration(self.item_selected, "rjpeg", rsr = rsr_sim)
        else: 
            QMessageBox.information(
                self,
                "Calibration in Progress",
                "A calibration is already in progress. Please wait for it to finish before starting a new one."
            )
    
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
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred while selecting directory."
            )
            return
        else:
            QMessageBox.information(
                self,
                "Directory Selected",
                f"You selected:\n{directory}"
                )
            # Adding directory name to loaded options for user to choose
            self.list_of_files.append(directory)
            self.AddDirectoryToTree(directory)

            # Enabling Tabs if they have not been enabled
            self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.indexOf(self.ui.calTab), True)
            self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.indexOf(self.ui.stabilityTab), True)
            self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.indexOf(self.ui.imageTab), True)

            # Validating image files so the slider can load them in.
            self.current_dir_files = sorted([
            os.path.join(directory, f)
            for f in os.listdir(directory)
            ])
            Factory = lit.ImageDataFactory()
            list_of_valid_files = [f for f in self.current_dir_files if Factory.is_valid_image_file(f, "rjpeg")]
            num_files = len(list_of_valid_files)
            self.ui.frameSelection.setMinimum(0)
            self.ui.frameSelection.setMaximum(max(0, num_files - 1))

    def OnTreeClicked(self, item, column):
        data = item.data(0, Qt.UserRole)

        if isinstance(data, str) and os.path.isfile(data):
            # disk file

            # Find index of file in current_dir_files
            try:
                self.index = self.current_dir_files.index(data)
            except ValueError:
                self.index = 0

            self.item_selected = data
            self.ui.frameSelection.setValue(self.index)
        elif isinstance(data, lit.ImageData):   # your image class
            # in-memory image
            qimg = prepare_for_qt(data.raw_counts)
            self.ui.imagelabel.setPixmap(QPixmap.fromImage(qimg))
        elif isinstance(data, str) and os.path.isdir(data):
            # Directory
            self.item_selected = data
            print(data)

    def ViewImage(self):
        if not self.item_selected:
            return

        Factory = lit.ImageDataFactory()
        config = lit.ImageDataConfig(
            filename=self.item_selected,
            fileformat="rjpeg"
        )

        self.current_image = Factory.create_from_file(config)

        qimg = prepare_for_qt(self.current_image.raw_counts)
        pixmap = QPixmap.fromImage(qimg)

        self.ui.imagelabel.setPixmap(pixmap)
        self.ui.labelFrameCount.setText(f"Current Frame: {self.index+1} of {len(self.current_dir_files)}.")

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

        self.active_calibration = True

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
        # Add to Variables section
        var_item = QTreeWidgetItem(self.varsRoot)
        var_item.setText(0, os.path.basename(self.item_selected))

        # Store the ACTUAL image object
        var_item.setData(0, Qt.UserRole, cal_array)

        QMessageBox.information(
            self,
            "Calibration Finished",
            "Blackbody calibration completed successfully."
        )
        self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.indexOf(self.ui.nedtTab), True)
        
        pixel_stats = prepare_pixel(cal_array, 1, 1)
        
        self.ViewCalibrationInfo(pixel_stats)

        self.active_calibration = False

    def ViewCalibrationInfo(self, pixel_stats):
        axs = self.calCanvas.get_axes_grid()

        individual_pixel = pixel_stats[0]
        means = pixel_stats[1]
        first_derivative = pixel_stats[2]
        second_derivative = pixel_stats[3]
        average_x_vals = pixel_stats[4]
        step_averages = pixel_stats[5]
        band_radiances = pixel_stats[6]
        gain = pixel_stats[7]
        bias = pixel_stats[8]
        row = pixel_stats[9]
        col = pixel_stats[10]
        chunk_size = pixel_stats[11]

        # ---- 1 ----
        axs[0,0].plot(individual_pixel)
        axs[0,0].set_title(f"")
        axs[0,0].set_xlabel("Frame number")
        axs[0,0].set_ylabel("Digital Count")

        # ---- 3 ----
        axs[1,0].plot(first_derivative)
        # axs[1,0].set_title("First derivative of Pixel")
        axs[1,0].set_xlabel("Frame number")
        axs[1,0].set_ylabel("Digital Count/Frame")

        # ---- 4 ----
        axs[1,1].plot(second_derivative)
        # axs[1,1].set_title("Second derivative of Pixel")
        axs[1,1].set_xlabel("Frame number")
        axs[1,1].set_ylabel("Digital Count/Frame^2")

        # ---- 5 ----
        axs[0,2].scatter(
            range(len(individual_pixel)),
            individual_pixel,
            c='blue', s=2, marker='o',
            label='collected data'
        )
        axs[0,2].scatter(
            average_x_vals,
            step_averages,
            c='red', s=30, marker='o',
            label='averages'
        )
        # axs[0,2].set_title("Averaged step levels over raw data")
        axs[0,2].legend()
        axs[0,2].set_xlabel("Frame number")
        axs[0,2].set_ylabel("Digital Count")

        # ---- 6 ----
        axs[1,2].scatter(
            step_averages,
            band_radiances,
            c='blue',
            label='Averaged Data'
        )

        axs[1,2].plot(
            step_averages,
            gain * step_averages + bias,
            c='red',
            label='line of best fit'
        )

        # axs[1,2].set_title("Integrated BB radiance vs DC")
        axs[1,2].legend()
        axs[1,2].set_xlabel("Digital Count")
        axs[1,2].set_ylabel("Band Radiance [W/m^2/sr]")

        self.calCanvas.figure.suptitle(f"Pixel statistics over time at location ({row},{col})")

        self.calCanvas.figure.tight_layout()
        self.calCanvas.draw()

    def SaveImage(self):
        # Add to Variables section
        var_item = QTreeWidgetItem(self.varsRoot)
        var_item.setText(0, os.path.basename(self.item_selected))

        # Store the ACTUAL image object
        var_item.setData(0, Qt.UserRole, self.current_image)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
