from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class canvasMatplot(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = plt.figure(tight_layout=True)
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
