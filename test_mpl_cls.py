import sys
from PyQt5 import QtWidgets, QtCore
from mpl_cls import MplWidget
import numpy as np
from PyQt5.QtCore import Qt, QSize


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.add_plot()



    def add_plot(self):

        temp= QtWidgets.QApplication.desktop().screenGeometry()
        width=temp.width()//2-50
        height=temp.height()//2-50



        scroll_area=QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        scroll_widget=QtWidgets.QWidget(scroll_area)
        layout = QtWidgets.QGridLayout(self)
        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)

        widget = MplWidget(parent=self)
        widget.setFixedWidth(width)
        widget.setFixedHeight(height)
        axes = widget.canvas.fig.add_subplot(111)

        objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
        y_pos = np.arange(len(objects))
        performance = [10, 8, 6, 4, 2, 1]

        axes.bar(y_pos, performance, align='center', alpha=0.5)
        axis=axes.twiny
        layout.addWidget(widget,0,0)


        widget = MplWidget(parent=self)
        widget.setFixedWidth(width)
        widget.setFixedHeight(height)
        axes = widget.canvas.fig.add_subplot(111)
        axes.plot([0, 1, 2, 3, 4], np.random.random(5))
        layout.addWidget(widget,0,1)

        widget = MplWidget(parent=self)
        widget.setFixedWidth(width)
        widget.setFixedHeight(height)
        axes = widget.canvas.fig.add_subplot(111)
        axes.plot([0, 1, 2, 3, 4], np.random.random(5))
        layout.addWidget(widget,1,0)

        widget = MplWidget(parent=self)
        widget.setFixedWidth(width)
        widget.setFixedHeight(height)
        axes = widget.canvas.fig.add_subplot(111)
        axes.plot([0, 1, 2, 3, 4], np.random.random(5))
        layout.addWidget(widget,1,1)

        widget = MplWidget(parent=self)
        widget.setFixedWidth(width)
        widget.setFixedHeight(height)
        axes = widget.canvas.fig.add_subplot(111)
        axes.plot([0, 1, 2, 3, 4], np.random.random(5))
        layout.addWidget(widget,2,0)

        widget = MplWidget(parent=self)
        widget.setFixedWidth(width)
        widget.setFixedHeight(height)
        axes = widget.canvas.fig.add_subplot(111)
        axes.plot([0, 1, 2, 3, 4], np.random.random(5))
        layout.addWidget(widget,2,1)

        widget = MplWidget(parent=self)
        widget.setFixedWidth(width)
        widget.setFixedHeight(height)
        axes = widget.canvas.fig.add_subplot(111)
        axes.plot([0, 1, 2, 3, 4], np.random.random(5))
        layout.addWidget(widget,2,2)

        self.setCentralWidget(scroll_area)

        # self.height = self.screenRect.height()
        # self.width = self.screenRect.width()

        # print()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
