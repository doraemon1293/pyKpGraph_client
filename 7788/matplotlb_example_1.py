import sys
import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)


class MplWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(MplWidget, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.canvas = MplCanvas(parent=layout, width=width, height=height, dpi=dpi)
        self.toolbar = NavigationToolbar(self.canvas, None)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        # toolbar = NavigationToolbar(sc, self)
        #
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(toolbar)
        # layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QGridLayout(central_widget)
        central_widget.setLayout(layout)
        widget = MplWidget()
        fig = widget.canvas.fig
        axes = fig.add_subplot(111)
        axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        layout.addWidget(widget, 0, 0)

        widget = MplWidget()
        fig = widget.canvas.fig
        axes = fig.add_subplot(111)
        axes.plot([5, 6, 7, 8, 9], [10, 1, 20, 3, 40])
        layout.addWidget(widget, 0, 1)

        widget = MplWidget()
        fig = widget.canvas.fig
        axes = fig.add_subplot(111)
        axes.plot([5, 6, 7, 8, 9], [10, 1, 20, 3, 40])
        layout.addWidget(widget, 1, 1)

        widget = MplWidget()
        fig = widget.canvas.fig
        axes = fig.add_subplot(111)
        axes.plot([5, 6, 7, 8, 9], [10, 1, 20, 3, 40])
        layout.addWidget(widget, 2, 0)

        widget = MplWidget()
        fig = widget.canvas.fig
        axes = fig.add_subplot(111)
        axes.plot([5, 6, 7, 8, 9], [10, 1, 20, 3, 40])
        layout.addWidget(widget, 2, 1)

        widget = MplWidget()
        fig = widget.canvas.fig
        axes = fig.add_subplot(111)
        axes.plot([5, 6, 7, 8, 9], [10, 1, 20, 3, 40])
        layout.addWidget(widget, 3, 0)


        #
        # widget = MplWidget()
        # fig=widget.canvas.fig
        # axes=fig.add_subplot(111)
        # axes.plot([5,6,7,8,9], [10,1,20,3,40])
        # layout.addWidget(widget,row=)

        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
