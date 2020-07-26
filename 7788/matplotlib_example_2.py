import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

class Window(QtWidgets.QMainWindow):
    def __init__(self, fig):
        self.qapp = QtWidgets.QApplication([])

        QtWidgets.QMainWindow.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QVBoxLayout())
        self.widget.layout().setContentsMargins(0,0,0,0)
        self.widget.layout().setSpacing(0)

        self.fig = fig
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.canvas.mpl_connect("resize_event", self.resize)

        self.widget.layout().addWidget(self.canvas)

        self.nav = NavigationToolbar(self.canvas, self.widget, coordinates=False)
        self.nav.setMinimumWidth(300)
        self.nav.setStyleSheet("QToolBar { border: 0px }")

        self.show()
        self.qapp.exec_()

    def resize(self, event):
        # on resize reposition the navigation toolbar to (0,0) of the axes.
        x,y = self.fig.axes[0].transAxes.transform((0,0))
        figw, figh = self.fig.get_size_inches()
        ynew = figh*self.fig.dpi-y - self.nav.frameGeometry().height()
        self.nav.move(x,ynew)

# create a figure with a subplot
fig, ax = plt.subplots(figsize=(5,3))
# colorize figure and axes to make transparency obvious
fig.set_facecolor("#e9c9ef")
ax.set_facecolor("#f7ecf9")
ax.plot([2,3,5,1], color="#ab39c1")
fig.tight_layout()

# pass the figure to the custom window
a = Window(fig)