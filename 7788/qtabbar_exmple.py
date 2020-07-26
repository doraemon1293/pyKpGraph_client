from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class TabBar(QTabBar):

    def tabSizeHint(self, index):
        if index == self.count() - 1:
            size = QSize(0, 0)
            for i in range(self.count() - 1):
                size += QTabBar.tabSizeHint(self, i)
            return QSize(self.width() - size.width(), size.height())
        else:
            return QTabBar.tabSizeHint(self, index)


app = QApplication([])

w = QWidget()
layout = QHBoxLayout()

leftLayout = QVBoxLayout()
rightLayout = QVBoxLayout()

leftLayout.addWidget(QTextEdit())

tabBar = TabBar()
tabBar.addTab("Hippo")
tabBar.addTab("Giraffe")

tempLayout = QHBoxLayout()
tempLayout.addWidget(tabBar)

rightLayout.addLayout(tempLayout)
rightLayout.addWidget(QListView())

layout.addLayout(leftLayout)
layout.addLayout(rightLayout)
w.setLayout(layout)

w.show()
app.exec_()