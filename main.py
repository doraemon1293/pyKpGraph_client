import sys
import traceback
import openpyxl
from PyQt5 import QtWidgets, QtCore, QtGui
from ui_Mainwindow import Ui_MainWindow
import mpl_cls
import pymongo
import collections
import util
import pandas as pd
import re
from sub_tab import Sub_tab
import os

MONGO_CLIENT_URL = "mongodb://localhost:27017/"
DB_NAME = "mydatabase"
AUTO_COMPLETE_LENGTH = 5
PERMANENT_SUBTAB_NO = 3
CHARTS_TAB_NAMES = {"HUAWEI2G_Hourly_tab", "HUAWEI2G_Daily_tab", "HUAWEI4G_Hourly_tab", "HUAWEI4G_Daily_tab",
                    "HUAWEI5G_Hourly_tab", "HUAWEI5G_Daily_tab"}


class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(MyMainWindow, self).__init__(parent)
        self.reload_template_file("template.xlsx")

    def reload_template_file(self, filename):
        if hasattr(self, "centralwidget"):
            temp = self.centralwidget
            filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open template", os.getcwd(), "*.xlsx")[0]
        else:
            temp = None

        if filename != "":
            self.setupUi(self)
            self.init()
            self.connect()
            self.load_config(filename=filename)
            self.build_tab_widgets()
            self.showMaximized()
            if temp != None:
                temp.deleteLater()

    def init(self):
        self.mongo_client = pymongo.MongoClient(MONGO_CLIENT_URL)
        self.cell_line_edit_autocompleter = QtWidgets.QCompleter()
        self.cell_line_edit_autocompleter_model = QtGui.QStandardItemModel()
        self.cell_line_edit_autocompleter.setModel(self.cell_line_edit_autocompleter_model)
        self.cell_line_edit.setCompleter(self.cell_line_edit_autocompleter)
        self.site_line_edit_autocompleter = QtWidgets.QCompleter()
        self.site_line_edit_autocompleter_model = QtGui.QStandardItemModel()
        self.site_line_edit_autocompleter.setModel(self.site_line_edit_autocompleter_model)
        self.site_line_edit.setCompleter(self.site_line_edit_autocompleter)

        self.start_date_time_edit.setCalendarPopup(True)
        self.end_date_time_edit.setCalendarPopup(True)
        self.start_date_edit = QtWidgets.QDateEdit(self.centralwidget)
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.hide()
        self.end_date_edit = QtWidgets.QDateEdit(self.centralwidget)
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.hide()

        self.start_date_time_edit.setDateTime(QtCore.QDateTime.fromString('2020/7/23 00:00:00', 'yyyy/M/d hh:mm:ss'))
        self.end_date_time_edit.setDateTime(QtCore.QDateTime.fromString('2020/7/24 00:00:00', 'yyyy/M/d hh:mm:ss'))
        self.start_date_edit.setDateTime(QtCore.QDateTime.fromString('2020/7/23', 'yyyy/M/d'))
        self.end_date_edit.setDateTime(QtCore.QDateTime.fromString('2020/7/29', 'yyyy/M/d'))

        self.cell_line_edit.setText("38298NAn781")
        self.site_line_edit.setText("38298N")
        self.scrollaleChartsAreas = {}
        self.sun_tabs = {}

    def load_config(self, filename):
        '''
        Load aggregation function
        Load tagwidget layout and chart layout and formula
        :param filename:
        :return:
        '''

        # init
        self.agg_function = {}
        self.charts_config = collections.OrderedDict()
        wb = openpyxl.load_workbook(filename=filename)
        for ws in wb.worksheets:
            # load agg function
            # if KPI in self.agg_function use agg_function else use sum
            if ws.title == "agg":
                rows = ws.rows
                next(rows)
                for row in rows:
                    kpi_name, agg = row[0].value, row[1].value
                    kpi_name = kpi_name.replace(".", "_")
                    self.agg_function[kpi_name] = agg

            # load charts tab config
            # self.charts_config 为3层级的字典
            # self.charts{config[tab_level_1][tab_level_2][chart_NO]
            if ws.title in CHARTS_TAB_NAMES:
                rows = ws.rows
                title = [cell.value for cell in next(rows)]
                self.charts_config[ws.title] = collections.OrderedDict()
                for row in rows:
                    if row[0].value:
                        d = {}
                        row = [cell.value for cell in row]
                        for i, s in enumerate(title):
                            d[s] = row[i]
                        formula = d["Formula"]
                        kpis, eval_exp = util.compile_formula(formula)
                        d["kpis"] = kpis
                        d["eval_exp"] = eval_exp
                        self.charts_config[ws.title].setdefault(d["Tab"], {})
                        self.charts_config[ws.title][d["Tab"]].setdefault(d["Chart_no"], [])
                        self.charts_config[ws.title][d["Tab"]][d["Chart_no"]].append(d)

    def build_tab_widgets(self):
        ''' build tab_level1 as per template 小时级和天极只建一个tab

        :return:
        '''

        self.scrollaleChartsAreas = {}
        self.sub_tabs = {}
        # create sub_tabs
        for tab_name1 in CHARTS_TAB_NAMES:
            tab1 = self.__getattribute__(tab_name1)
            # todo add operation related to Sub_tab
            if tab_name1 in self.charts_config:
                configs = self.charts_config[tab_name1]
                for ind, tab_name2 in enumerate(configs.keys()):
                    # tab2 = QtWidgets.QWidget(tab1)
                    # sc = mpl_cls.ScrollaleChartsArea(tab2)
                    # layout = QtWidgets.QHBoxLayout()
                    # layout.addWidget(sc)
                    # layout.setContentsMargins(0, 0, 0, 0)
                    # tab2.setLayout(layout)
                    # tab2.sc=sc
                    # tab1.insertTab(ind,tab2, tab_name2)

                    tab2 = mpl_cls.ScrollaleChartsArea(tab1)
                    tab2.setObjectName(tab_name2)
                    tab1.insertTab(ind, tab2, tab_name2)
                    self.scrollaleChartsAreas[tab_name1, tab_name2] = tab2

            for i in range(tab1.count()):
                tab = tab1.widget(i)
                tab_name2 = tab.objectName()
                self.sub_tabs[tab_name1, tab_name2] = tab

    def connect(self):
        self.actionExport_All_CHarts_to_Excel.triggered.connect(self.export_all_charts_to_excel)
        self.actionReload_Template.triggered.connect(self.reload_template_file)
        self.query_push_btn.clicked.connect(self.on_query_push_btn_clicked)
        self.tabwidget_level1.currentChanged.connect(self.on_tabwidget_level1_currentChanged)
        self.cell_line_edit.textEdited.connect(self.on_cell_line_edit_textEdited)
        self.site_line_edit.textEdited.connect(self.on_site_line_edit_textEdited)

    # QtCore.QMetaObject.connectSlotsByName(self)

    def export_all_charts_to_excel(self):
        print("todo")

    def clear_sc(self):
        for sc in self.scrollaleChartsAreas.values():
            sc.recreate()

    def on_query_push_btn_clicked(self):
        if self.cell_radio_btn.isChecked():
            query_level = "cell"
        elif self.site_radio_btn.isChecked():
            query_level = "site"
        elif self.cluster_radio_btn.isChecked():
            query_level = "cluster"

        tab1 = self.tabwidget_level1.currentWidget()
        tab1_name = tab1.objectName()
        if tab1_name in CHARTS_TAB_NAMES:
            self.statusbar.showMessage("Loading Data from Server")

            # initiate sc
            project = {}
            agg = {}
            for tab2_name in self.charts_config.get(tab1_name, {}):
                tab1.findChild(mpl_cls.ScrollaleChartsArea, tab2_name).recreate()
                for chart_no in self.charts_config[tab1_name][tab2_name]:
                    for config in self.charts_config[tab1_name][tab2_name][chart_no]:
                        for kpi in config["kpis"]:
                            project[kpi] = 1
                            agg[kpi] = self.agg_function.get(kpi, "sum")

            if "Hourly" in tab1_name:
                time_col = "Time"
                GP = 3600
                st = self.start_date_time_edit.dateTime().toPyDateTime()
                end = self.end_date_time_edit.dateTime().toPyDateTime()
                if tab1_name.startswith("HUAWEI5G"):
                    collection_name = "NR_CELLS_HOURLY"
            if "Daily" in tab1_name:
                time_col = "Date"
                GP = 3600 * 24
                st = self.start_date_edit.dateTime().toPyDateTime()
                end = self.end_date_edit.dateTime().toPyDateTime()
                if tab1_name.startswith("HUAWEI5G"):
                    collection_name = "NR_CELLS_DAILY"

            if query_level == "cell":
                column_name = "Cell Name"
                column_value = self.cell_line_edit.text().strip()

            if query_level == "site":
                if tab1_name.startswith("HUAWEI5G"):
                    column_name = "gNodeB Name"  # todo need to consider 2/3/4G
                    column_value = self.site_line_edit.text().strip()  # todo need to consider 2/3/4G
            # todo cluster

            myclient = pymongo.MongoClient(MONGO_CLIENT_URL)
            col = myclient[DB_NAME][collection_name]

            project[time_col] = 1
            project[column_name] = 1
            query = {column_name: column_value,
                     time_col: {"$gte": st, "$lte": end}}
            res = list(col.find(query, project))
            if res:
                df = pd.DataFrame(res)
                df["GP"] = GP
                if query_level == "site":
                    for kpi in set(agg):
                        if kpi not in df.columns:
                            del agg[kpi]
                            print("missing {} in databse for {}".format(kpi, column_value))
                    df = df.groupby([time_col, column_name], as_index=False).agg(agg)

                for tab2_name in self.charts_config.get(tab1_name,{}):
                    sc = tab1.findChild(mpl_cls.ScrollaleChartsArea, tab2_name)
                    configs = self.charts_config[tab1_name][tab2_name]
                    sc.plot(configs, df, GP, column_value, time_col)
                self.statusbar.showMessage("{} {} query finished".format(column_value, tab1_name, 60000))
            else:
                self.statusbar.showMessage("{} doesn't have data".format(column_value))
                # todo cluster
            myclient.close()

    def on_tabwidget_level1_currentChanged(self, i):
        tab_name = self.tabwidget_level1.widget(i).objectName()
        if "Hourly" in tab_name:
            self.gridLayout.replaceWidget(self.start_date_edit, self.start_date_time_edit)
            self.gridLayout.replaceWidget(self.end_date_edit, self.end_date_time_edit)
            self.start_date_edit.hide()
            self.end_date_edit.hide()
            self.start_date_time_edit.show()
            self.end_date_time_edit.show()
        elif "Daily" in tab_name:
            self.gridLayout.replaceWidget(self.start_date_time_edit, self.start_date_edit)
            self.gridLayout.replaceWidget(self.end_date_time_edit, self.end_date_edit)
            self.start_date_time_edit.hide()
            self.end_date_time_edit.hide()
            self.start_date_edit.show()
            self.end_date_edit.show()

    # autocomplet on cell line edit
    def on_cell_line_edit_textEdited(self, s):
        COLLETION_NAME = None
        arr = []
        s = self.cell_line_edit.text()
        if len(s) >= 2:
            current_tab = self.tabwidget_level1.currentWidget().objectName()
            if current_tab.startswith("HUAWEI5G"):
                COLLETION_NAME = "NR_CELL_NAMES"
            # todo set COLLECTION_NAME for 2g/3g/4g
            if COLLETION_NAME:
                mycol = self.mongo_client[DB_NAME][COLLETION_NAME]
                query = {"_id": re.compile("^{}".format(s), re.IGNORECASE)}
                arr = [d["_id"] for d in mycol.find(query, sort=[("_id", 1)])]
        self.cell_line_edit_autocompleter_model.clear()
        for text in arr:
            self.cell_line_edit_autocompleter_model.appendRow(QtGui.QStandardItem(text))

    # autocomplet on site line edit
    def on_site_line_edit_textEdited(self, s):
        COLLETION_NAME = None
        arr = []
        s = self.site_line_edit.text()
        if len(s) >= 2:
            current_tab = self.tabwidget_level1.currentWidget().objectName()
            if current_tab.startswith("HUAWEI5G"):
                COLLETION_NAME = "NR_GNODEB_NAMES"
            # todo set COLLECTION_NAME for 2g/3g/4g
            if COLLETION_NAME:
                mycol = self.mongo_client[DB_NAME][COLLETION_NAME]
                query = {"_id": re.compile("^{}".format(s), re.IGNORECASE)}
                arr = [d["_id"] for d in mycol.find(query, sort=[("_id", 1)])]
        self.site_line_edit_autocompleter_model.clear()
        for text in arr:
            self.site_line_edit_autocompleter_model.appendRow(QtGui.QStandardItem(text))

    def contextMenuEvent(self, event):
        contextMenu = QtWidgets.QMenu(self)
        export_all_charts_act = contextMenu.addAction("Export All to Excel")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        # if action == quitAct:
        #     self.close()

    def closeEvent(self, event):
        self.mongo_client.close()


if __name__ == "__main__":
    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("error catched!:")
        print("error message:\n", tb)
        QtWidgets.QApplication.quit()
        # or QtWidgets.QApplication.exit(0)


    sys.excepthook = excepthook

    app = QtWidgets.QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
