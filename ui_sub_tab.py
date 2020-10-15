# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sub_tabnfjFFk.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PyQt5.QtWidgets import *


class Ui_sub_tab(object):
    def setupUi(self, sub_tab):
        if sub_tab.objectName():
            sub_tab.setObjectName(u"sub_tab")
        sub_tab.resize(400, 300)
        self.multicells_tab = QWidget()
        self.multicells_tab.setObjectName(u"multicells_tab")
        sub_tab.addTab(self.multicells_tab, "")
        self.worstcells_tab = QWidget()
        self.worstcells_tab.setObjectName(u"worstcells_tab")
        sub_tab.addTab(self.worstcells_tab, "")
        self.export_tab = QWidget()
        self.export_tab.setObjectName(u"export_tab")
        sub_tab.addTab(self.export_tab, "")

        self.retranslateUi(sub_tab)

        sub_tab.setCurrentIndex(0)

    # setupUi

    def retranslateUi(self, sub_tab):
        sub_tab.setWindowTitle(QCoreApplication.translate("sub_tab", u"TabWidget", None))
        sub_tab.setTabText(sub_tab.indexOf(self.multicells_tab), QCoreApplication.translate("sub_tab", u"Multi Cells", None))
        sub_tab.setTabText(sub_tab.indexOf(self.worstcells_tab), QCoreApplication.translate("sub_tab", u"Worst Cells", None))
        sub_tab.setTabText(sub_tab.indexOf(self.export_tab), QCoreApplication.translate("sub_tab", u"Export", None))
    # retranslateUi

