# importing the required libraries 

from PyQt5.QtWidgets import *
from PyQt5 import QtCore 
from PyQt5 import QtGui 
from PyQt5 import QtWidgets
import sys
import time
import sys
import traceback
class Window(QMainWindow): 
    def __init__(self):
        super().__init__()

        # set the title
        self.setWindowTitle("Memory")

        # setting the geometry of window
        self.setGeometry(0, 0, 400, 300)

        # creating a label widget
        self.lay = QHBoxLayout()

        # moving position
        # self.label_1.move(100, 100)
        #
        # # setting up border
        # self.label_1 = QLabel("Label2", self)
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.widget=QWidget(self.tab_widget)
        self.tab_widget.addTab(self.widget,"tab")


        self.btn=QtWidgets.QPushButton("btn",parent=self)
        self.btn.setObjectName("btn")
        self.btn.move(100,100)

        self.btn1=QtWidgets.QPushButton("btn1",parent=self)
        self.btn1.setObjectName("bttn")
        self.btn1.move(200,100)


        self.show()
        QtCore.QMetaObject.connectSlotsByName(self)

        # delete reference

        # show all the widgets
    @QtCore.pyqtSlot()

    def on_btn_clicked(self):
        print("1")
        self.tab_widget.deleteLater()
    @QtCore.pyqtSlot()
    def on_bttn_clicked(self):
        print("2")
        self.setCentralWidget(self.widget)
        print(self.widget)


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    QtWidgets.QApplication.quit()
    # or QtWidgets.QApplication.exit(0)


sys.excepthook = excepthook

# create pyqt5 app 
App = QApplication(sys.argv) 

# create the instance of our Window 
window = Window() 

# start the app 
sys.exit(App.exec())


