import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureManagerQT
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar2


class ViewWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # create a simple main widget to keep the figure
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        layout = QVBoxLayout()
        self.mainWidget.setLayout(layout)

        # create a figure
        self.figure_canvas = FigureManagerQT(Figure())
        layout.addWidget(self.figure_canvas, 10)

        # and the axes for the figure
        self.axes = self.figure_canvas.figure.add_subplot(111)

        # add a navigation toolbar
        # self.navigation_toolbar = NavigationToolbar2(self.figure_canvas, self)
        # layout.addWidget(self.navigation_toolbar, 0)

        # create a simple widget to extend the navigation toolbar
        anotherWidget = QLineEdit()
        # add the new widget to the existing navigation toolbar
        self.navigation_toolbar.addWidget(anotherWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = ViewWidget()
    mw.show()
    sys.exit(app.exec_())