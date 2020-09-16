import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def window():
    app = QApplication(sys.argv)
    win = QWidget()
    grid = QGridLayout()

    grid.addWidget(QPushButton("B1"), 1, 0)
    grid.addWidget(QPushButton("B2"), 1, 2)
    grid.addWidget(QPushButton("B3"), 1, 1)

    grid.addWidget(QPushButton("B3"), 2,1,1,2)
    win.setLayout(grid)
    win.setGeometry(100, 100, 200, 100)
    win.setWindowTitle("PyQt")
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()
