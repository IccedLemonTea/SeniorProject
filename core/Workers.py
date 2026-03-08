# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, Signal
import LWIRImageTool as lit
import numpy as np


class CalibrationWorker(QObject):
    progress = Signal(str, int, int)   # phase, current, total
    finished = Signal(object)          # calibration array
    error = Signal(str)

    def __init__(self, directory : str, filetype, rsr: str=None, bb_start_temp=None, bb_temp_step=None):
        super().__init__()
        self.directory = directory
        self.filetype = filetype
        self.rsr = rsr
        self.bb_start_temp = bb_start_temp
        self.bb_temp_step = bb_temp_step
    def run(self):
        factory = lit.CalibrationDataFactory()

        config = lit.BlackbodyCalibrationConfig(
            directory=self.directory,
            filetype=self.filetype,
            blackbody_temperature=self.bb_start_temp,
            temperature_step=self.bb_temp_step,
            rsr=self.rsr,
            progress_cb=self._progress_callback
        )

        result = factory.create(config)
        self.finished.emit(result)

    def _progress_callback(self, phase, current, total):
        self.progress.emit(phase, current, total)


class StabilityWorker(QObject):
    progress = Signal(str, int, int)   # phase, current, total
    finished = Signal(object)          # processed 1D mean array
    error = Signal(str)

    def __init__(self, directory : str, filetype: str ="rjpeg"):
        super().__init__()
        self.directory = directory
        self.filetype = filetype

    def run(self):
        try:
            image_stack = lit.stack_images(
                self.directory,
                filetype=self.filetype,
                progress_cb=self._progress_callback
            )

            # Signal a brief processing phase for the mean computation
            self.progress.emit("processing", 0, 1)
            result = np.mean(image_stack, axis=(0, 1))
            self.progress.emit("processing", 1, 1)

            self.finished.emit(result)

        except Exception as e:
            self.error.emit(str(e))

    def _progress_callback(self, phase, current, total):
        self.progress.emit(phase, current, total)