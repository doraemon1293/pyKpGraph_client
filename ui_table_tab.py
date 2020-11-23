# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'table_tabCwKIMJ.ui'
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

from sort_and_filter_tbl_view import Sort_and_filter_tbl_view


class Ui_Table_tab(object):
    def setupUi(self, Table_tab):
        if Table_tab.objectName():
            Table_tab.setObjectName(u"Table_tab")

        self.layoutWidget = QWidget(Table_tab)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 30, 331, 230))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.object_label = QLabel(self.layoutWidget)
        self.object_label.setObjectName(u"object_label")

        self.horizontalLayout.addWidget(self.object_label)

        self.date_range_label = QLabel(self.layoutWidget)
        self.date_range_label.setObjectName(u"date_range_label")

        self.horizontalLayout.addWidget(self.date_range_label)

        self.checkBox_day_by_day = QCheckBox(self.layoutWidget)
        self.checkBox_day_by_day.setObjectName(u"checkBox_day_by_day")

        self.horizontalLayout.addWidget(self.checkBox_day_by_day)

        self.export_to_csv_btn = QPushButton(self.layoutWidget)
        self.export_to_csv_btn.setObjectName(u"export_to_csv_btn")

        self.horizontalLayout.addWidget(self.export_to_csv_btn)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.sort_and_filter_tbl_view = Sort_and_filter_tbl_view(self.layoutWidget)
        self.sort_and_filter_tbl_view.setObjectName(u"sort_and_filter_tbl_view")

        self.verticalLayout.addWidget(self.sort_and_filter_tbl_view)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Table_tab)
    # setupUi

    def retranslateUi(self, Table_tab):
        Table_tab.setWindowTitle(QCoreApplication.translate("Table_tab", u"Form", None))
        self.object_label.setText(QCoreApplication.translate("Table_tab", u"TextLabel", None))
        self.date_range_label.setText(QCoreApplication.translate("Table_tab", u"TextLabel", None))
        self.checkBox_day_by_day.setText(QCoreApplication.translate("Table_tab", u"Day By Day", None))
        self.export_to_csv_btn.setText(QCoreApplication.translate("Table_tab", u"Export to CSV", None))
    # retranslateUi
