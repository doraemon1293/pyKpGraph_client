import sys
import traceback
import openpyxl
from PyQt5 import QtWidgets, QtCore
from ui_Mainwindow import Ui_MainWindow
import mpl_cls
import pymongo
import collections
import util
import pandas as pd

MONGO_CLIENT_URL = "mongodb://localhost:27017/"
DB_NAME = "mydatabase"
COLLECTIONS_NAME = "NR_CELLS_HOURLY"


class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.connect()
        self.load_config(filename="template.xlsx")
        self.build_tab_level1_layout()
        self.showMaximized()

        self.tabwidgets = {}
        self.scrollaleChartsAreas = {}

        self.start_date_time_edit.setDateTime(QtCore.QDateTime.fromString('2020/4/26 00:00:00', 'yyyy/M/d hh:mm:ss'))
        self.end_date_time_edit.setDateTime(QtCore.QDateTime.fromString('2020/4/27 00:00:00', 'yyyy/M/d hh:mm:ss'))
        self.cell_line_edit.setText("99415NCn781")

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
            if ws.title == "agg":
                rows = ws.rows
                next(rows)
                for row in rows:
                    kpi, agg = row[0].value, row[1].value
                    if kpi:
                        kpi.replace(".", "_")
                        self.agg_function[kpi] = agg
                    else:
                        break

            # load chart config
            # self.charts_config 为3层级的字典
            if ws.title in ("HUAWEI5G_Hourly", "HUAWEI5G_Daily"):
                rows = ws.rows
                title = [cell.value for cell in next(rows)]
                self.charts_config[ws.title] = {}
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
            # print(self.charts_config)

    def build_tab_level1_layout(self):
        ''' build tab_level1 as per template 小时级和天极只建一个tab

        :return:
        '''
        # remove old wodgets from memory
        
        for sc_name in self.scrollaleChartsAreas:
            self.scrollaleChartsAreas[sc_name].deletelater()
            del self.scrollaleChartsAreas[sc_name]

        for widget_name in self.tabwidgets:
            self.tabwidgets[widget_name].deletelater()
            del self.tabwidgets[widget_name]

        for tab_name in self.charts_config:
            if self.granularity_combo_box.currentText() in tab_name:
                self.tabwidgets[tab_name] = QtWidgets.QTabWidget(self.tabwidget_level1)
                self.tabwidgets[tab_name].setObjectName(tab_name)
                self.tabwidget_level1.insertTab(self.tabwidget_level1.count() - 2, self.tabwidgets[tab_name], tab_name)
                self.tabwidget_level1.setCurrentWidget(self.tabwidgets[tab_name])

    def build_tab_level2_layout(self):
        '''根据当前粒度是小时还是天建二级tab

        :return:
        '''

        for tab_name_full in self.charts_config:
            if self.granularity_combo_box.currentText() in tab_name_full:
                tab_name = tab_name_full.split("_")[0]
                for tab_name1 in self.charts_config[tab_name_full]:
                    self.tabwidgets[tab_name, tab_name1] = QtWidgets.QWidget(self.tabwidgets[tab_name])
                    self.tabwidgets[tab_name].insertTab(self.tabwidgets[tab_name].count(),
                                                        self.tabwidgets[tab_name, tab_name1], tab_name1)
                    sc = mpl_cls.ScrollaleChartsArea(self.tabwidgets[tab_name, tab_name1])
                    layout = QtWidgets.QHBoxLayout()
                    layout.addWidget(sc)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.tabwidgets[tab_name, tab_name1].setLayout(layout)
                    self.scrollaleChartsAreas[tab_name, tab_name1] = sc

    def connect(self):
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.pyqtSlot()
    def on_query_push_btn_clicked(self):
        self.statusbar.showMessage("Loading Data from Server")
        self.build_tab_level2_layout()
        # print(self.tabWidget.currentIndex())

        if self.cell_radio_btn.isChecked():
            query_level = "cell"
        elif self.site_radio_btn.isChecked():
            query_level = "site"
        elif self.cluster_radio_btn.isChecked():
            query_level = "cluster"
        current_tab = self.tabwidget_level1.currentWidget().objectName()
        if current_tab in ("HUAWEI5G",):
            config_key = current_tab + "_" + self.granularity_combo_box.currentText()
            # initiate sc
            for sc in self.scrollaleChartsAreas.values():
                sc.recreate()
            project = {}
            for tab in self.charts_config[config_key]:
                for chart_no in self.charts_config[config_key][tab]:
                    for config in self.charts_config[config_key][tab][chart_no]:
                        for kpi in config["kpis"]:
                            project[kpi] = 1

            if self.granularity_combo_box.currentText() == "Hourly":
                time_col = "Time"
                GP = 3600
                if current_tab == "HUAWEI5G":
                    collection_name = "NR_CELLS_HOURLY"
                    myclient = pymongo.MongoClient(MONGO_CLIENT_URL)
                    col = myclient[DB_NAME][collection_name]
            # else: #todo daily level

            project[time_col] = 1

            if query_level == "cell":
                project["Cell Name"] = 1

                st = self.start_date_time_edit.dateTime().toPyDateTime()
                end = self.end_date_time_edit.dateTime().toPyDateTime()
                cell_name = self.cell_line_edit.text().strip()
                query = {"Cell Name": cell_name,
                         time_col: {"$gte": st, "$lte": end}}
                res = list(col.find(query, project))
                if res:
                    df = pd.DataFrame(res)
                    df["GP"] = GP
                    for tab in self.charts_config[config_key]:
                        sc = self.scrollaleChartsAreas[current_tab, tab]
                        configs = self.charts_config[config_key][tab]
                        sc.plot(configs, df)
                    self.statusbar.showMessage(
                        "{} {} query finished".format(cell_name, self.granularity_combo_box.currentText()), 60000)
                else:
                    self.statusbar.showMessage("Cell {} doesn't exist".format(cell_name))

            if query_level == "site":
                project["gNodeB Name"] = 1

                st = self.start_date_time_edit.dateTime().toPyDateTime()
                end = self.end_date_time_edit.dateTime().toPyDateTime()
                cell_name = self.cell_line_edit.text().strip()
                query = {"Cell Name": cell_name,
                         time_col: {"$gte": st, "$lte": end}}
                res = list(col.find(query, project))
                if res:
                    df = pd.DataFrame(res)
                    df["GP"] = GP
                    for tab in self.charts_config[config_key]:
                        sc = self.scrollaleChartsAreas[current_tab, tab]
                        configs = self.charts_config[config_key][tab]
                        sc.plot(configs, df)
                    self.statusbar.showMessage(
                        "{} {} query finished".format(cell_name, self.granularity_combo_box.currentText()), 60000)
                else:
                    self.statusbar.showMessage("Cell {} doesn't exist".format(cell_name))
            myclient.close()

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
