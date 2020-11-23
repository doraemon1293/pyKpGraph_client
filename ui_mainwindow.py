# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainwindowVCnBFD.ui'
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

from sub_tab import Sub_tab

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(811, 600)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionExport_All_CHarts_to_Excel = QAction(MainWindow)
        self.actionExport_All_CHarts_to_Excel.setObjectName(u"actionExport_All_CHarts_to_Excel")
        self.actionReload_Template = QAction(MainWindow)
        self.actionReload_Template.setObjectName(u"actionReload_Template")
        self.actionCluster_Definition = QAction(MainWindow)
        self.actionCluster_Definition.setObjectName(u"actionCluster_Definition")
        self.actionChange_Date_Line = QAction(MainWindow)
        self.actionChange_Date_Line.setObjectName(u"actionChange_Date_Line")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.site_line_edit = QLineEdit(self.centralwidget)
        self.site_line_edit.setObjectName(u"site_line_edit")

        self.horizontalLayout_2.addWidget(self.site_line_edit)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.layer_combo_box = QComboBox(self.centralwidget)
        self.layer_combo_box.setObjectName(u"layer_combo_box")

        self.horizontalLayout_2.addWidget(self.layer_combo_box)


        self.horizontalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)

        self.cell_radio_btn = QRadioButton(self.centralwidget)
        self.cell_radio_btn.setObjectName(u"cell_radio_btn")
        self.cell_radio_btn.setChecked(True)

        self.gridLayout.addWidget(self.cell_radio_btn, 0, 0, 1, 1)

        self.cluster_radio_btn = QRadioButton(self.centralwidget)
        self.cluster_radio_btn.setObjectName(u"cluster_radio_btn")

        self.gridLayout.addWidget(self.cluster_radio_btn, 0, 2, 1, 1)

        self.site_radio_btn = QRadioButton(self.centralwidget)
        self.site_radio_btn.setObjectName(u"site_radio_btn")

        self.gridLayout.addWidget(self.site_radio_btn, 1, 0, 1, 1)

        self.end_date_time_edit = QDateTimeEdit(self.centralwidget)
        self.end_date_time_edit.setObjectName(u"end_date_time_edit")

        self.gridLayout.addWidget(self.end_date_time_edit, 1, 5, 1, 1)

        self.cell_line_edit = QLineEdit(self.centralwidget)
        self.cell_line_edit.setObjectName(u"cell_line_edit")

        self.gridLayout.addWidget(self.cell_line_edit, 0, 1, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 4, 1, 1)

        self.start_date_time_edit = QDateTimeEdit(self.centralwidget)
        self.start_date_time_edit.setObjectName(u"start_date_time_edit")

        self.gridLayout.addWidget(self.start_date_time_edit, 0, 5, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 1, 4, 1, 1)

        self.query_push_btn = QPushButton(self.centralwidget)
        self.query_push_btn.setObjectName(u"query_push_btn")

        self.gridLayout.addWidget(self.query_push_btn, 0, 6, 1, 1)

        self.cluster_combo_box = QComboBox(self.centralwidget)
        self.cluster_combo_box.setObjectName(u"cluster_combo_box")
        self.cluster_combo_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.gridLayout.addWidget(self.cluster_combo_box, 0, 3, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.tabwidget_level1 = QTabWidget(self.centralwidget)
        self.tabwidget_level1.setObjectName(u"tabwidget_level1")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabwidget_level1.sizePolicy().hasHeightForWidth())
        self.tabwidget_level1.setSizePolicy(sizePolicy)
        self.tabwidget_level1.setDocumentMode(True)
        self.HUAWEI2G_Daily_tab = Sub_tab()
        self.HUAWEI2G_Daily_tab.setObjectName(u"HUAWEI2G_Daily_tab")
        self.tabwidget_level1.addTab(self.HUAWEI2G_Daily_tab, "")
        self.HUAWEI4G_Daily_tab = Sub_tab()
        self.HUAWEI4G_Daily_tab.setObjectName(u"HUAWEI4G_Daily_tab")
        self.tabwidget_level1.addTab(self.HUAWEI4G_Daily_tab, "")
        self.HUAWEI5G_Daily_tab = Sub_tab()
        self.HUAWEI5G_Daily_tab.setObjectName(u"HUAWEI5G_Daily_tab")
        self.tabwidget_level1.addTab(self.HUAWEI5G_Daily_tab, "")
        self.HUAWEI2G_Hourly_tab = Sub_tab()
        self.HUAWEI2G_Hourly_tab.setObjectName(u"HUAWEI2G_Hourly_tab")
        self.tabwidget_level1.addTab(self.HUAWEI2G_Hourly_tab, "")
        self.HUAWEI4G_Hourly_tab = Sub_tab()
        self.HUAWEI4G_Hourly_tab.setObjectName(u"HUAWEI4G_Hourly_tab")
        self.tabwidget_level1.addTab(self.HUAWEI4G_Hourly_tab, "")
        self.HUAWEI5G_Hourly_tab = Sub_tab()
        self.HUAWEI5G_Hourly_tab.setObjectName(u"HUAWEI5G_Hourly_tab")
        self.tabwidget_level1.addTab(self.HUAWEI5G_Hourly_tab, "")
        self.report = QWidget()
        self.report.setObjectName(u"report")
        self.tabwidget_level1.addTab(self.report, "")
        self.maitainence = QWidget()
        self.maitainence.setObjectName(u"maitainence")
        self.tabwidget_level1.addTab(self.maitainence, "")

        self.verticalLayout.addWidget(self.tabwidget_level1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 811, 26))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menuMenu.addAction(self.actionReload_Template)
        self.menuMenu.addAction(self.actionExport_All_CHarts_to_Excel)
        self.menuMenu.addAction(self.actionCluster_Definition)
        self.menuMenu.addAction(self.actionChange_Date_Line)
        self.menuMenu.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.tabwidget_level1.setCurrentIndex(3)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionExport_All_CHarts_to_Excel.setText(QCoreApplication.translate("MainWindow", u"Export All CHarts to Excel", None))
        self.actionReload_Template.setText(QCoreApplication.translate("MainWindow", u"Reload Template", None))
        self.actionCluster_Definition.setText(QCoreApplication.translate("MainWindow", u"Cluster Definition", None))
        self.actionChange_Date_Line.setText(QCoreApplication.translate("MainWindow", u"Change Date Line", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Layer", None))
        self.cell_radio_btn.setText(QCoreApplication.translate("MainWindow", u"Cell", None))
        self.cluster_radio_btn.setText(QCoreApplication.translate("MainWindow", u"Cluster", None))
        self.site_radio_btn.setText(QCoreApplication.translate("MainWindow", u"Site", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"End", None))
        self.query_push_btn.setText(QCoreApplication.translate("MainWindow", u"Query", None))
        self.tabwidget_level1.setTabText(self.tabwidget_level1.indexOf(self.HUAWEI2G_Daily_tab), QCoreApplication.translate("MainWindow", u"2G_Daily", None))
        self.tabwidget_level1.setTabText(self.tabwidget_level1.indexOf(self.HUAWEI4G_Daily_tab), QCoreApplication.translate("MainWindow", u"4G_Daily", None))
        self.tabwidget_level1.setTabText(self.tabwidget_level1.indexOf(self.HUAWEI5G_Daily_tab), QCoreApplication.translate("MainWindow", u"5G_Daily", None))
        self.tabwidget_level1.setTabText(self.tabwidget_level1.indexOf(self.HUAWEI2G_Hourly_tab), QCoreApplication.translate("MainWindow", u"2G_Hourly", None))
        self.tabwidget_level1.setTabText(self.tabwidget_level1.indexOf(self.HUAWEI4G_Hourly_tab), QCoreApplication.translate("MainWindow", u"4G_Hourly", None))
        self.tabwidget_level1.setTabText(self.tabwidget_level1.indexOf(self.HUAWEI5G_Hourly_tab), QCoreApplication.translate("MainWindow", u"5G_Hourly", None))
        self.tabwidget_level1.setTabText(self.tabwidget_level1.indexOf(self.report), QCoreApplication.translate("MainWindow", u"Report", None))
        self.tabwidget_level1.setTabText(self.tabwidget_level1.indexOf(self.maitainence), QCoreApplication.translate("MainWindow", u"Maitainence", None))
        self.menuMenu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
    # retranslateUi


