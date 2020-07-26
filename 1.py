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
#
# class Color2(QWidget):
#     def __init__(self, color, *args, **kwargs):
#         super(Color2, self).__init__(*args, **kwargs)
#         self.setAutoFillBackground(True)
#         palette = self.palette()
#         palette.setColor(QPalette.Window, QColor(color))
#         self.setPalette(palette)
#         self.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
#
#     def minimumSizeHint(self):
#         return QSize(250,150)
#
# class MyTableWidget(QWidget):
#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.layout = QVBoxLayout(self)
#         self.tabs = QTabWidget(self)
#         self.layout.addWidget(self.tabs)
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
#         self.table_widget.addTab(self.tab1, "Tab1")
#         self.table_widget.addTab(self.tab2, "Tab2")
#         lay = QVBoxLayout(self.tab1)
#
#         self.scrollArea = QScrollArea()
#         lay.addWidget(self.scrollArea)
#         self.scrollArea.setWidgetResizable(True)
#         self.scrollAreaWidgetContents = QWidget()
#         self.scrollArea.setWidget(self.scrollAreaWidgetContents)
#
#         self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
#         self.verticalLayout.addWidget(Color2('blue'))
#         self.verticalLayout.addWidget(Color2('red'))
#         self.verticalLayout.insertStretch(-1)
#         self.verticallayout2 = QVBoxLayout(self.tab2)
#         self.verticallayout2.addWidget(Color2('green'))
#
#         self.scrollArea.setWidget(self.scrollAreaWidgetContents)
#
#         self.setCentralWidget(self.table_widget)
#         self.show()
#
# if __name__ == '__main__':
#
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())




def f(x,y,**kwargs):
    print(kwargs)
    # print(x,y,a,b,c)

f(1,2,**{"a":3,"b":4,"c":5})