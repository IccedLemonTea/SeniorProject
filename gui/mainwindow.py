# This Python file uses the following encoding: utf-8

import sys
import os
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QApplication, QInputDialog, QMainWindow, QFileDialog, QMessageBox, QListWidget, QListWidgetItem, QLabel, QTreeWidgetItem
from PySide6.QtCore import QObject, Signal, Qt, QThread
import LWIRImageTool as lit
from core.Workers import CalibrationWorker
from core.image_display import prepare_for_qt
from core.plot_canvas import MplCanvas
from core.pixel_stats import prepare_pixel
from core.calibration_dialog import CalibrationDialog
from core.project_serializer import save_project, load_project
from core.select_RSR import select_rsr
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
        self.index = None
        self.active_stability = False
        self.list_of_image_files = [] 
        self.selected_rsr_path = None
        self.active_NEdT = None
        self.calibration_data = None
        self.NEdT_Data = None
        self.stability_data = None
        self.loading_project = False

        # ---- Matplotlib canvas inside calibration tab ----
        self.calCanvas = MplCanvas(self.ui.calibrationPlotContainer)
        self.ui.calPlotLayout.addWidget(self.calCanvas)

        self.stabilityCanvas = MplCanvas(self.ui.stabilityPlotContainer)
        self.ui.stabilityPlotLayout.addWidget(self.stabilityCanvas)

        self.nedtCanvas = MplCanvas(self.ui.widgetNEDTPlot)
        self.ui.layoutNEDTPlot.addWidget(self.nedtCanvas)

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
        self.ui.frameSelection.sliderReleased.connect(self.UpdateSliderVal)
        self.filesRoot = self.ui.widgetProjectTreeList.topLevelItem(0)
        self.varsRoot  = self.ui.widgetProjectTreeList.topLevelItem(1)
        self.ui.saveImage.clicked.connect(self.SaveImage)
        self.ui.nextFrame.clicked.connect(self.NextFrame)
        self.ui.priorFrame.clicked.connect(self.PriorFrame)
        self.ui.rowTextEdit.textChanged.connect(self.OnPixelInputChanged)
        self.ui.colTextEdit.textChanged.connect(self.OnPixelInputChanged)
        self.ui.texteditNEDTCol.textChanged.connect(self.OnPixelInputChanged)
        self.ui.texteditNEDTRow.textChanged.connect(self.OnPixelInputChanged)
        self.ui.actionSave_Project.triggered.connect(self.SaveProject)
        self.ui.actionOpen_Project.triggered.connect(self.LoadProject)
        self.ui.actionOpenOther.triggered.connect(self.OpenOther)
        self.ui.pushSaveCal.clicked.connect(self.SaveCalPlot)
        self.ui.pushSaveNEDT.clicked.connect(self.SaveNEdTPlot)


# ───── FILE AND DIRECTORY HANDLING ──────────────────────────────────────────────────────
    def OpenOther(self):
        # QFileDialog for opening other types of files (e.g. txts for RSR)
        filepath,_ = QFileDialog.getOpenFileName(
            self,
            "Select file path",
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
            list_item = QTreeWidgetItem(self.filesRoot)
            list_item.setText(0, os.path.basename(filepath))
            list_item.setData(0, Qt.UserRole, filepath)

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
            current_dir_files = sorted([
            os.path.join(directory, f)
            for f in os.listdir(directory)
            ])
            
            Factory = lit.ImageDataFactory()

            # Look at files in directory, determine filetype of imagery (ASSUMES IMAGERY IS SORTED FIRST)
            self.filetype = Factory.get_image_filetype(current_dir_files[0])
            # Validates the rest of the directory
            self.list_of_image_files = [f for f in current_dir_files if Factory.is_valid_image_file(f, self.filetype)]

            # Setting bounds for QSlider
            num_files = len(self.list_of_image_files)
            self.ui.frameSelection.setMinimum(0)
            self.ui.frameSelection.setMaximum(max(0, num_files - 1))

            # Loading first image to image viewer
            self.index = 0
            self.OnFrameChanged()

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

# ───── PROJECT TREE HANDLING ──────────────────────────────────────────────────────
    def AddDirectoryToTree(self, directory):
        root = QTreeWidgetItem(self.filesRoot)
        root.setText(0, os.path.basename(directory))
        root.setData(0, Qt.UserRole, directory)

        for fname in sorted(os.listdir(directory)):
            child = QTreeWidgetItem(root)
            child.setText(0, fname)
            child.setData(0, Qt.UserRole, os.path.join(directory, fname))

        root.setExpanded(False)

    def AddFileToTree(self, file):
        list_item = QTreeWidgetItem(self.filesRoot)
        list_item.setText(0, os.path.basename(file))
        list_item.setData(0, Qt.UserRole, file)
        
    def OnTreeClicked(self, item, column):
        data = item.data(0, Qt.UserRole)
        if isinstance(data, str) and os.path.isfile(data):
            # Find index of file in list_of_image_files
            try:
                self.index = self.list_of_image_files.index(data)
                self.OnFrameChanged()
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
            ImageFactory = lit.ImageDataFactory()
            self.filetype = ImageFactory.get_image_filetype(os.path.join(data, os.listdir(data)[0]))

# ───── IMAGE DISPLAY TAB ──────────────────────────────────────────────────────
    def ViewImage(self):
        if not self.item_selected:
            return

        Factory = lit.ImageDataFactory()
        filetype = Factory.get_image_filetype(self.item_selected)
        config = lit.ImageDataConfig(
            filename=self.item_selected,
            fileformat=filetype
        )

        self.current_image = Factory.create_from_file(config)

        qimg = prepare_for_qt(self.current_image.raw_counts)
        pixmap = QPixmap.fromImage(qimg)

        self.ui.imagelabel.setPixmap(pixmap)
        self.ui.labelFrameCount.setText(f"Current Frame: {self.index+1} of {len(self.list_of_image_files)}.")

    def NextFrame(self):
        if self.index < len(self.list_of_image_files):
            self.index = self.index + 1
            self.ui.frameSelection.setValue(self.index)
            self.OnFrameChanged()
              
    def PriorFrame(self):

        if self.index > 0:
            self.index = self.index -1
            self.ui.frameSelection.setValue(self.index)
            self.OnFrameChanged()

    def UpdateSliderVal(self):
        self.index = self.ui.frameSelection.value()
        self.OnFrameChanged()

    def OnFrameChanged(self):
        if 0 <= self.index < len(self.list_of_image_files):
            self.item_selected = self.list_of_image_files[self.index]
            self.ViewImage()

# ───── CALIBRATION DISPLAY TAB ──────────────────────────────────────────────────────
    def Calibration(self):
        if not self.active_calibration:
            reply = QMessageBox.question(
                self,
                "Calibration",
                "Do you want to perform a calibration run?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.No:
                return   # User chickened out
            # Open advanced dialog
            dlg = CalibrationDialog(self)

            if os.path.isdir(self.item_selected):
                if dlg.exec():   # User pressed Start
                    settings = dlg.getValues()

                    environment_temp = float(settings["environment_temp"])
                    bb_start_temp = float(settings["bb_start_temp"])
                    bb_temp_step = float(settings["bb_temp_step"])

                    self.bb_start_temp = bb_start_temp
                    self.bb_temp_step = bb_temp_step

                    if settings["use_rsr"]:
                        self.selected_rsr_path = select_rsr(self.filesRoot, self)
                        if self.selected_rsr_path is None:
                            return  # user cancelled or no file found
                        self.StartCalibration(self.item_selected, self.filetype, rsr=self.selected_rsr_path, bb_start_temp=bb_start_temp, bb_temp_step=bb_temp_step, environmental_temperature=environment_temp)
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

                        self.StartCalibration(self.item_selected, self.filetype, rsr=rsr_sim, bb_start_temp=bb_start_temp, bb_temp_step=bb_temp_step, environmental_temperature=environment_temp)
                else:
                    QMessageBox.critical(
                    self,
                    "Error",
                    f"The current item selected in the Project Files is not a directory.")
                    return
        else: 
            QMessageBox.information(
                self,
                "Calibration in Progress",
                "A calibration is already in progress. Please wait for it to finish before starting a new one."
            )

    def StartCalibration(self, directory, filetype, rsr=None, bb_start_temp=None, bb_temp_step=None, environmental_temperature = None):
        self.thread = QThread()
        self.worker = CalibrationWorker(directory, filetype, rsr, bb_start_temp, bb_temp_step, environmental_temperature)

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
        self.ui.progressbarCal.setValue(0)
        self.ui.progressbarCal.setFormat("Starting calibration...")

        self.thread.start()

        self.active_calibration = True

    def CalibrationFinished(self, cal_array):
        self.ui.progressbarCal.setValue(100)
        self.ui.progressbarCal.setFormat("Calibration complete")

        self.calibration_data = cal_array
        # Add to Variables section
        var_item = QTreeWidgetItem(self.varsRoot)
        var_item.setText(0, str(os.path.basename(self.item_selected) + "_calibration"))

        # Store the ACTUAL image object
        var_item.setData(0, Qt.UserRole, cal_array)

        QMessageBox.information(
            self,
            "Calibration Finished",
            "Blackbody calibration completed successfully."
        )
        self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.indexOf(self.ui.nedtTab), True)
        
        row = int(self.ui.rowTextEdit.toPlainText())
        col = int(self.ui.colTextEdit.toPlainText())
        pixel_stats = prepare_pixel(cal_array, row, col)
        
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
        axs[0].scatter(
            range(len(individual_pixel)),
            individual_pixel,
            c='blue', s=2, marker='o',
            label='collected data'
        )
        axs[0].scatter(
            average_x_vals,
            step_averages,
            c='red', s=30, marker='o',
            label='averages'
        )
        for step in range(self.calibration_data._number_of_steps):
            start = int(self.calibration_data._array_of_avg_coords[2 * step])
            end   = int(self.calibration_data._array_of_avg_coords[2 * step + 1])
            axs[0].axvspan(start, end, alpha=0.15, color='gray')
        axs[0].legend()
        axs[0].grid()
        axs[0].set_xlabel("Frame number")
        axs[0].set_ylabel("Digital Count")

        # ---- 6 ----
        axs[1].scatter(
            step_averages,
            band_radiances,
            c='blue',
            label='Averaged Data'
        )

        axs[1].plot(
            step_averages,
            gain * step_averages + bias,
            c='red',
            label=f'Fit line (y={gain:.4f}x + {bias:.4f})'
        )

        # axs[1,2].set_title("Integrated BB radiance vs DC")
        axs[1].legend()
        axs[1].grid()
        axs[1].set_xlabel("Digital Count")
        axs[1].set_ylabel("Band Radiance [W/m^2/sr]")

        self.calCanvas.figure.suptitle(f"Pixel statistics over time at location ({row},{col})")

        self.calCanvas.figure.tight_layout()
        self.calCanvas.draw()

    def SaveCalPlot(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Calibration Plot",
            "",
            "PNG (*.png);;PDF (*.pdf);;SVG (*.svg)"
        )
        if file_path:
            self.calCanvas.figure.savefig(file_path, dpi=300, bbox_inches='tight')

# ───── NEDT CALCULATION AND DISPLAY TAB ──────────────────────────────────────────────────────
    def NEdTCalc(self):
        if not self.selected_rsr_path:
            self.selected_rsr_path = select_rsr(self.filesRoot, self)
        if not self.selected_rsr_path:
            return
        
        txt_content = np.loadtxt(self.selected_rsr_path, skiprows=1, delimiter=',')
        wavelengths = txt_content[:, 0]
        response = txt_content[:, 1]

        self.temps = self.calibration_data.blackbody_temperature + self.calibration_data.temperature_step * np.arange(self.calibration_data._number_of_steps)
        self.NEdT_Data = lit.NEDT.NEdT_calculation(self.calibration_data.image_stack, self.calibration_data.coefficients, self.temps, wavelengths, response)

        # Add to Variables section
        var_item = QTreeWidgetItem(self.varsRoot)
        var_item.setText(0, str(os.path.basename(self.item_selected) + "_NEdT_array"))

        # Store the ACTUAL image object
        var_item.setData(0, Qt.UserRole, self.NEdT_Data)
        
        # Image-wide percentiles across all pixels at each temperature step
        self.median_NEDT  = np.percentile(self.NEdT_Data, 50,  axis=(0,1))  # same as median
        self.active_NEdT = True
        self.ViewNEDTInfo(self.NEdT_Data[0,0,:], self.temps)

    def ViewNEDTInfo(self, nedt_pixel, temps, row=1, col=1):
        axs = self.nedtCanvas.get_single_grid()

        # Image-wide std band around median
        std_NEDT = np.std(self.NEdT_Data, axis=(0,1))
        upper = self.median_NEDT + std_NEDT
        lower = self.median_NEDT - std_NEDT

        axs.fill_between(temps, lower, upper, alpha=0.20, color='gray', label='Image median ± 1s')
        axs.plot(temps, self.median_NEDT, c='gray', label='Image NEdT50', linewidth=2, marker='o', markersize=4)

        # Selected pixel
        axs.plot(temps, nedt_pixel, c='blue', label=f'Pixel ({row},{col}) NEdT68', linewidth=2, marker='o', markersize=4)

        axs.legend()
        axs.set_title(f"NEdT Confidence Intervals at Pixel ({row},{col})")
        axs.set_xlabel("Temperature Step [K]")
        axs.set_ylabel("NEdT [K]")
        axs.grid(True, linestyle='--', alpha=0.4)
        self.nedtCanvas.figure.tight_layout()
        self.nedtCanvas.draw()

    def SaveNEdTPlot(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save NEdT Plot",
            "",
            "PNG (*.png);;PDF (*.pdf);;SVG (*.svg)"
        )
        if file_path:
            self.nedtCanvas.figure.savefig(file_path, dpi=300, bbox_inches='tight')

# ───── STABILITY ANALYSIS TAB ──────────────────────────────────────────────────────
    def Stability(self):
        if not self.active_stability:
            reply = QMessageBox.question(
                self,
                "Stability Analysis",
                "Do you want to perform a stability analysis?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.No:
                return   # User chickened out
            if isinstance(self.item_selected, str) and os.path.isdir(self.item_selected):
                self.StartStability(self.item_selected)
        else:
            QMessageBox.information(
                self,
                "Stability Analysis in Progress",
                "A stability analysis is already in progress. Please wait for it to finish before starting a new one."
            )

    def StartStability(self, directory):
        from core.Workers import StabilityWorker  # already imported at top if you prefer

        self.stability_thread = QThread()
        self.stability_worker = StabilityWorker(directory, filetype= self.filetype)

        self.stability_worker.moveToThread(self.stability_thread)

        # Wiring
        self.stability_thread.started.connect(self.stability_worker.run)
        self.stability_worker.progress.connect(self.UpdateStabilityProgress)
        self.stability_worker.finished.connect(self.StabilityFinished)
        self.stability_worker.error.connect(self.StabilityError)

        # Cleanup
        self.stability_worker.finished.connect(self.stability_thread.quit)
        self.stability_worker.finished.connect(self.stability_worker.deleteLater)
        self.stability_thread.finished.connect(self.stability_thread.deleteLater)
        self.stability_worker.error.connect(self.stability_thread.quit)

        # UI state
        self.ui.progressbarStability.setValue(0)
        self.ui.progressbarStability.setFormat("Starting stability analysis...")

        self.stability_thread.start()

    def UpdateStabilityProgress(self, phase, current, total):
        if total > 0:
            percent = int((current / total) * 100)
        else:
            percent = 0

        if phase == "loading":
            self.ui.progressbarStability.setRange(0, 100)
            self.ui.progressbarStability.setFormat("Stacking images... %p%")
        elif phase == "processing":
            self.ui.progressbarStability.setRange(0, 100)
            self.ui.progressbarStability.setFormat("Computing mean... %p%")

        self.ui.progressbarStability.setValue(percent)

    def StabilityFinished(self, result):
        self.ui.progressbarStability.setRange(0, 100)
        self.ui.progressbarStability.setValue(100)
        self.ui.progressbarStability.setFormat("Stability analysis complete")

        ax = self.stabilityCanvas.get_single_grid()
        ax.plot(result)
        ax.set_title("Mean pixel value across frames")
        ax.set_xlabel("Frame number")
        ax.set_ylabel("Mean Digital Count")
        self.stabilityCanvas.draw()

        self.stability_data = result
        # Add to Variables section
        var_item = QTreeWidgetItem(self.varsRoot)
        var_item.setText(0, str(os.path.basename(self.item_selected) + "_stability"))

        # Store the ACTUAL image object
        var_item.setData(0, Qt.UserRole, result)

        QMessageBox.information(
            self,
            "Stability Finished",
            "Stability run completed successfully."
        )
    
    def StabilityError(self, message):
        self.ui.progressbarStability.setRange(0, 100)
        self.ui.progressbarStability.setValue(0)
        self.ui.progressbarStability.setFormat("Error")
        QMessageBox.critical(self, "Stability Error", f"An error occurred:\n{message}")

# ───── HELPER FUNCTIONS ───────────────────────────────────────────────────────
    def UpdateProgress(self, phase, current, total):
        percent = int((current / total) * 100)

        if phase == "loading":
            self.ui.progressbarCal.setFormat("Loading images... %p%")
        elif phase == "calibrating":
            self.ui.progressbarCal.setFormat("Calibrating pixels... %p%")
        elif phase == "ascension":
            self.ui.progressbarCal.setFormat("Calculating ascension regions... %p%")

        self.ui.progressbarCal.setValue(percent)

    def OnPixelInputChanged(self):
        tab_index = self.ui.tabWidget.currentIndex()
        if tab_index == 1:  # Calibration tab is active
            if hasattr(self, 'calibration_data') and self.calibration_data is not None:
                try:
                    row = int(self.ui.rowTextEdit.toPlainText())
                    col = int(self.ui.colTextEdit.toPlainText())
                except ValueError:
                    return  # Invalid input, ignore the change
                row = self.calibration_data.coefficients.shape[0] - 1 if row >= self.calibration_data.coefficients.shape[0] else row
                col = self.calibration_data.coefficients.shape[1] - 1 if col >= self.calibration_data.coefficients.shape[1] else col
                row = 0 if row < 0 else row
                col = 0 if col < 0 else col
                pixel_stats = prepare_pixel(self.calibration_data, row, col)
                self.ui.labelGainCoeff.setText(f"{pixel_stats[7]:.4f}")
                self.ui.labelBiasCoeff.setText(f"{pixel_stats[8]:.4f}")
                self.ViewCalibrationInfo(pixel_stats)

        elif tab_index == 2: # NEdT tab is active
            if hasattr(self, 'NEdT_Data') and self.NEdT_Data is not None:
                try:
                    row = int(self.ui.texteditNEDTRow.toPlainText())
                    col = int(self.ui.texteditNEDTCol.toPlainText())
                except ValueError:
                    return  # Invalid input, ignore the change
                row = self.NEdT_Data.shape[0] - 1 if row >= self.NEdT_Data.shape[0] else row
                col = self.NEdT_Data.shape[1] - 1 if col >= self.NEdT_Data.shape[1] else col
                row = 0 if row < 0 else row
                col = 0 if col < 0 else col
                nedt_pixel = self.NEdT_Data[row, col,:]
                self.ViewNEDTInfo(nedt_pixel, self.temps, row=row, col=col)

    def OnTabChanged(self, index):
        """Triggered when tab is switched"""

        # Skips tab changes when loading an old project
        if self.loading_project == True:
            self.loading_project = False
            return None
        
        # Act based on index or label
        if index == 0:
            return
        elif index == 1:
            self.Calibration()
        elif index == 2:
            if not self.active_NEdT:
                self.NEdTCalc()
        elif index == 3:
            self.Stability()

# ───── PROJECT VARIABLES AND DATA HANDLING ──────────────────────────────────────────────────────
    def SaveImage(self):
        # Add to Variables section
        var_item = QTreeWidgetItem(self.varsRoot)
        var_item.setText(0, os.path.basename(self.item_selected))

        # Store the ACTUAL image object
        var_item.setData(0, Qt.UserRole, self.current_image)

# ───── PROJECT SAVE AND LOAD FUNCTIONALITY ──────────────────────────────────────────────────────
    def SaveProject(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select folder to save project into",
            self.home_dir,
        )

        if not folder_path:
            return

        # Default project subfolder name based on current directory selection
        default_name = (
        os.path.basename(self.item_selected)
        if self.item_selected else "lwir_project"
        )

        # Ask user to name the output directory
        dir_name, ok = QInputDialog.getText(
        self,
        "Name Output Directory",
        "Enter a name for the output directory:",
        text=default_name
        )

        if not ok or not dir_name.strip():
            return

        project_folder = os.path.join(folder_path, dir_name.strip())

        try:
            save_project(self, project_folder)
            QMessageBox.information(
                self,
                "Project Saved",
                f"Project saved to:\n{project_folder}\n\n"
                f"  project.json  — manifest\n"
                f"  arrays.npz    — calibration coefficients, image stack, stability data"
            )
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save project:\n{str(e)}")

    def LoadProject(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select project folder to open",
            self.home_dir,
        )

        if not folder_path:
            return

        try:
            load_project(self, folder_path)
            QMessageBox.information(
                self,
                "Project Loaded",
                f"Project loaded from:\n{folder_path}"
            )
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Load Error",
                                f"Could not find project files:\n{str(e)}\n\n"
                                f"Make sure you selected a folder containing project.json.")
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Failed to load project:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
