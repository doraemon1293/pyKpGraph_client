# # -*- coding: utf-8 -*-
# """
# Created on Fri Nov 17 07:07:08 2017
#
# @author: Erik
# """
#
# import sys
# from PyQt5.QtWidgets import QLayout, QVBoxLayout ,QTabWidget, QMainWindow,QApplication, QWidget, QSizePolicy, QScrollArea
# from PyQt5.QtGui import QColor, QPalette
# from PyQt5.QtCore import QSize
# class Color2(QWidget):
#
#     def __init__(self, color, *args, **kwargs):
#         super(Color2, self).__init__(*args, **kwargs)
#         self.setAutoFillBackground(True)
#         palette = self.palette()
#         palette.setColor(QPalette.Window, QColor(color))
#         self.setPalette(palette)
#         self.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
#
#     def sizeHint(self):
#         return QSize(250,150)
#
# class MyTableWidget(QWidget):
#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.layout = QVBoxLayout(self)
#         # Initialize tab screen
#         self.tabs = QTabWidget(self)
#         self.layout.addWidget(self.tabs)
#         #self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
#         #self.tabs.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
#
#     def addTab(self, widget, text):
#         self.tabs.addTab(widget, text)
#         widget.setAutoFillBackground(True)
#         my_yellow = QColor.fromHsl(35, 255, 153, 128 )
#         dark_blue = QColor.fromHsl(211, 196, 38, 255)
#         widget.palette().setColor(QPalette.Window, dark_blue)
#         widget.palette().setColor(QPalette.WindowText, my_yellow)
#
# class Example(QMainWindow):
#
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#
#         self.statusBar().showMessage('Ready')
#         self.setGeometry(300, 300, 250, 150)
#         self.setWindowTitle('Statusbar')
#         self.table_widget = MyTableWidget(self)
#         self.tab1 = QWidget()
#         self.tab2 = QWidget()
#         #self.tab1.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
#         self.table_widget.addTab(self.tab1, "Tab1")
#         self.table_widget.addTab(self.tab2, "Tab2")
#
#         self.scrollArea = QScrollArea(self.tab1)
#         #self.scrollArea = QScrollArea(self)
#         self.scrollArea.setWidgetResizable(True)
#         self.scrollAreaWidgetContents = QWidget(self.scrollArea)
#         #self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 247))
#         self.scrollAreaWidgetContents.setMinimumSize(QSize(1100, 1300))
#         #self.scrollAreaWidgetContents.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
#         #self.scrollAreaWidgetContents.setWidgetResizable(True)
#         #self.scrollArea.setWidget(self.scrollAreaWidgetContents)
#
#         self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
#         #self.verticalLayout.addWidget(self.scrollArea)
#         self.verticalLayout.addWidget(Color2('blue'))
#         self.verticalLayout.addWidget(Color2('red'))
#         self.verticalLayout.insertStretch(-1)
#         #self.verticalLayout.setSizeConstraint(1)#QLayout.SizeConstraint.setNoConstraint)
#         self.verticallayout2 = QVBoxLayout(self.tab2)
#         self.verticallayout2.addWidget(Color2('green'))
#
#         #self.scrollArea.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding))
#         self.scrollArea.setWidget(self.scrollAreaWidgetContents)
#
#         self.setCentralWidget(self.table_widget)
#         self.show()
#         print(self.table_widget.minimumSizeHint())
#
# if __name__ == '__main__':
#
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())


try:
    max([])
except ZeroDivisionError as e:
    print(e)
else:
    print(11)