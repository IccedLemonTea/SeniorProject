from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QRadioButton, QLineEdit, QHBoxLayout, QButtonGroup
)

class CalibrationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Calibration Options")
        self.setPalette(parent.palette())

        Hlayout = QHBoxLayout(self)
        Vlayout = QVBoxLayout()
        Templayout = QVBoxLayout()
        Hlayout.addLayout(Vlayout)
        Hlayout.addLayout(Templayout)

        # ───── Question 1 ─────────────────────────────────────────────────────
        Vlayout.addWidget(QLabel("Are you using a real RSR file?"))

        self.rsrYes = QRadioButton("Yes, I have an RSR")
        self.rsrNo = QRadioButton("No, simulate RSR")

        self.rsrYes.setChecked(True)

        self.group = QButtonGroup(self)
        self.group.addButton(self.rsrYes)
        self.group.addButton(self.rsrNo)

        Vlayout.addWidget(self.rsrYes)
        Vlayout.addWidget(self.rsrNo)

        # ───── Question 2 ─────────────────────────────────────────────────────
        Templayout.addWidget(QLabel("What is the temperature of your environment?"))
        self.tempInput = QLineEdit()
        self.tempInput.setPlaceholderText("e.g. 303.15.0 [K]")
        Templayout.addWidget(self.tempInput)
        Templayout.addWidget(QLabel("What is the starting temperature of your blackbody?"))
        self.bbTempInput = QLineEdit()
        self.bbTempInput.setPlaceholderText("e.g. 283.15 [K]")
        Templayout.addWidget(self.bbTempInput)
        Templayout.addWidget(QLabel("What are the temperature steps of your blackbody?"))
        self.tempStepInput = QLineEdit()
        self.tempStepInput.setPlaceholderText("e.g. 1.0 [K]")
        Templayout.addWidget(self.tempStepInput)

        # ──── FWHM Input ─────────────────────────────────────────────────────
        self.fwhmWLabel = QLabel("Enter FWHM width (µm):")
        self.fwhmWInput = QLineEdit()
        self.fwhmWInput.setPlaceholderText("e.g. 2.0")

        self.fwhmCLabel = QLabel("Enter FWHM center (µm):")
        self.fwhmCInput = QLineEdit()
        self.fwhmCInput.setPlaceholderText("e.g. 7.0")

        self.numSamplesLabel = QLabel("Number of samples")
        self.numSamplesInput = QLineEdit()
        self.numSamplesInput.setPlaceholderText("e.g. 1000")



        Vlayout.addWidget(self.fwhmWLabel)
        Vlayout.addWidget(self.fwhmWInput)
        Vlayout.addWidget(self.fwhmCLabel)
        Vlayout.addWidget(self.fwhmCInput)
        Vlayout.addWidget(self.numSamplesLabel)
        Vlayout.addWidget(self.numSamplesInput)

        # Hide by default (only show if NO selected)
        self.fwhmWLabel.hide()
        self.fwhmWInput.hide()
        self.fwhmCLabel.hide()
        self.fwhmCInput.hide()
        self.numSamplesInput.hide()
        self.numSamplesLabel.hide()

        # ──── Buttons ─────────────────────────────────────────────────────
        btnLayout = QHBoxLayout()
        self.okBtn = QPushButton("Start Calibration")
        self.cancelBtn = QPushButton("Cancel")

        btnLayout.addWidget(self.okBtn)
        btnLayout.addWidget(self.cancelBtn)

        Vlayout.addLayout(btnLayout)

        # ──── Connections ─────────────────────────────────────────────────────
        self.rsrNo.toggled.connect(self.toggleFWHM)
        self.okBtn.clicked.connect(self.accept)
        self.cancelBtn.clicked.connect(self.reject)

    def toggleFWHM(self, checked):
        self.fwhmWLabel.setVisible(checked)
        self.fwhmWInput.setVisible(checked)
        self.fwhmCLabel.setVisible(checked)
        self.fwhmCInput.setVisible(checked)
        self.numSamplesLabel.setVisible(checked)
        self.numSamplesInput.setVisible(checked)
    
        

    # Helper to return data cleanly
    def getValues(self):
        return {
            "use_rsr": self.rsrYes.isChecked(),
            "fwhm_width": self.fwhmWInput.text(),
            "fwhm_center": self.fwhmCInput.text(),
            "num_samples": self.numSamplesInput.text(),
            "environment_temp": self.tempInput.text(),
            "bb_start_temp": self.bbTempInput.text(),
            "bb_temp_step": self.tempStepInput.text()
        }
