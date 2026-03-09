from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

    def get_axes_grid(self):
        self.figure.clear()
        axs = self.figure.subplots(1, 2)
        return axs

    def get_single_grid(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        return ax

    def draw(self):
        self.canvas.draw()
