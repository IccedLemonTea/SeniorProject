from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QRadioButton, QLineEdit, QHBoxLayout, QButtonGroup
)

class CalibrationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Calibration Options")
        self.setPalette(parent.palette())

        layout = QVBoxLayout(self)

        # ---- Question 1 ----
        layout.addWidget(QLabel("Are you using a real RSR file?"))

        self.rsrYes = QRadioButton("Yes, I have an RSR")
        self.rsrNo = QRadioButton("No, simulate RSR")

        self.rsrYes.setChecked(True)

        self.group = QButtonGroup(self)
        self.group.addButton(self.rsrYes)
        self.group.addButton(self.rsrNo)

        layout.addWidget(self.rsrYes)
        layout.addWidget(self.rsrNo)

        # ---- FWHM Input ----
        self.fwhmWLabel = QLabel("Enter FWHM width (µm):")
        self.fwhmWInput = QLineEdit()
        self.fwhmWInput.setPlaceholderText("e.g. 2.0")

        self.fwhmCLabel = QLabel("Enter FWHM center (µm):")
        self.fwhmCInput = QLineEdit()
        self.fwhmCInput.setPlaceholderText("e.g. 7.0")

        self.numSamplesLabel = QLabel("Number of samples")
        self.numSamplesInput = QLineEdit()
        self.numSamplesInput.setPlaceholderText("e.g. 1000")



        layout.addWidget(self.fwhmWLabel)
        layout.addWidget(self.fwhmWInput)
        layout.addWidget(self.fwhmCLabel)
        layout.addWidget(self.fwhmCInput)
        layout.addWidget(self.numSamplesLabel)
        layout.addWidget(self.numSamplesInput)

        # Hide by default (only show if NO selected)
        self.fwhmWLabel.hide()
        self.fwhmWInput.hide()
        self.fwhmCLabel.hide()
        self.fwhmCInput.hide()
        self.numSamplesInput.hide()
        self.numSamplesLabel.hide()

        # ---- Buttons ----
        btnLayout = QHBoxLayout()
        self.okBtn = QPushButton("Start Calibration")
        self.cancelBtn = QPushButton("Cancel")

        btnLayout.addWidget(self.okBtn)
        btnLayout.addWidget(self.cancelBtn)

        layout.addLayout(btnLayout)

        # ---- Connections ----
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
            "num_samples": self.numSamplesInput.text()
        }
