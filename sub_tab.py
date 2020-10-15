
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
from ui_sub_tab import Ui_sub_tab
# Ui_sub_tab, QtBaseClass = uic.loadUiType("sub_tab.ui")

class Sub_tab(QTabWidget,Ui_sub_tab):
    def __init__(self, parent=None):
        super(Sub_tab, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":

    app = QApplication([])
    myWin = Sub_tab()
    myWin.show()
    sys.exit(app.exec_())
