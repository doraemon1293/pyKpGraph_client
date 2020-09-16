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
import db_operator

pd.options.display.max_columns = None
pd.options.display.max_rows = None

MONGO_CLIENT_URL = "mongodb://localhost:27017/"
DB_NAME = "mydatabase"
AUTO_COMPLETE_LENGTH = 5
PERMANENT_SUBTAB_NO = 3
CHARTS_TAB_NAMES = {"HUAWEI2G_Hourly_tab", "HUAWEI2G_Daily_tab", "HUAWEI4G_Hourly_tab", "HUAWEI4G_Daily_tab",
                    "HUAWEI5G_Hourly_tab", "HUAWEI5G_Daily_tab"}


class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(MyMainWindow, self).__init__(parent)
        self.not_init = True
        self.MONGO_CLIENT_URL = MONGO_CLIENT_URL
        self.reload_template_file("template.xlsx")

    def reload_template_file(self, filename):
        if self.not_init == True:
            self.setupUi(self)
            self.init()
            self.connect()
            self.load_config(filename=filename)
            self.build_tab_widgets()
            self.showMaximized()
            self.not_init = False
        else:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open template", os.getcwd(), "*.xlsx")[0]
            if filename != "":
                temp = self.centralwidget
                self.mongo_client.close()
                self.setupUi(self)
                self.init()
                self.connect()
                self.load_config(filename=filename)
                self.build_tab_widgets()
                self.showMaximized()
                if temp != None:
                    temp.deleteLater()

    def init(self):
        self.mongo_client = pymongo.MongoClient(self.MONGO_CLIENT_URL)
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

        self.cell_line_edit.setText("12723NAn781")
        self.site_line_edit.setText("12723N")
        self.scrollaleChartsAreas = {}
        self.sub_tabs = {}

    def load_config(self, filename):
        '''
        Load aggregation function
        Load tagwidget layout and chart layout and formula
        :param filename:
        :return:
        '''

        # init
        self.agg_function = {}
        self.charts_config = {}
        wb = openpyxl.load_workbook(filename=filename)
        for ws in wb.worksheets:
            # load agg function
            # if KPI in self.agg_function use agg_function else use sum
            if ws.title == "agg_function":
                df = pd.read_excel(filename, sheet_name=ws.title)
                for _, row in df.iterrows():
                    kpi_name, agg = row["kpi_name"], row["agg"]
                    kpi_name = kpi_name.replace(".", "_")
                    self.agg_function[kpi_name] = agg

            # load charts tab config
            if ws.title in CHARTS_TAB_NAMES:
                df = pd.read_excel(filename, sheet_name=ws.title)
                df = df.apply(util.compile_formula_in_df, axis=1)
                self.charts_config[ws.title] = df
            if ws.title == "additional_kpi":
                df = pd.read_excel(filename, sheet_name=ws.title)
                df = df.apply(util.compile_formula_in_df, axis=1)
                self.additional_kpi = df
            if ws.title == "conditional_kpi":
                df = pd.read_excel(filename, sheet_name=ws.title)
                df = df.apply(util.compile_formula_in_df, axis=1)
                self.conditional_kpi = df
            if ws.title == "auto_completer_Config":
                self.auto_completer_Config = pd.read_excel(filename, sheet_name=ws.title)
                self.auto_completer_Config = self.auto_completer_Config.set_index(["tab_name", "data_level"])
            if ws.title == "query_config":
                self.query_config = pd.read_excel(filename, sheet_name=ws.title)
            if ws.title == "small_legend_config":
                df = pd.read_excel(filename, sheet_name=ws.title)
                self.small_legend_config = {}
                for _, row in df.iterrows():
                    self.small_legend_config[row["Parameter"]] = row["Value"]
                self.small_legend_config["bbox_to_anchor"] = eval(self.small_legend_config["bbox_to_anchor"])
                self.small_legend_config["ncol"] = int(self.small_legend_config["ncol"])
                self.small_legend_config["fontsize"] = str(self.small_legend_config["fontsize"])


    def build_tab_widgets(self):
        ''' build tab_level1 as per template 小时级和天极只建一个tab

        :return:
        '''

        self.scrollaleChartsAreas = {}
        self.sub_tabs = {}
        # create sub_tabs
        for tab_name1 in self.charts_config:
            config_df = self.charts_config[tab_name1]
            tab1 = self.__getattribute__(tab_name1)
            ind = 0
            for tab_name2 in config_df["Tab"].unique():
                tab2 = mpl_cls.ScrollaleChartsArea(tab1)
                tab2.setObjectName(tab_name2)
                tab1.insertTab(ind, tab2, tab_name2)
                ind += 1
                self.scrollaleChartsAreas[tab_name1, tab_name2] = tab2

                # tab2 = QtWidgets.QWidget(tab1)
                # sc = mpl_cls.ScrollaleChartsArea(tab2)
                # layout = QtWidgets.QHBoxLayout()
                # layout.addWidget(sc)
                # layout.setContentsMargins(0, 0, 0, 0)
                # tab2.setLayout(layout)
                # tab2.sc=sc
                # tab1.insertTab(ind,tab2, tab_name2)

                # tab2 = mpl_cls.ScrollaleChartsArea(tab1)
                # tab2.setObjectName(tab_name2)
                # tab1.insertTab(ind, tab2, tab_name2)
                # self.scrollaleChartsAreas[tab_name1, tab_name2] = tab2

            # for i in range(tab1.count()):
            #     tab = tab1.widget(i)
            #     tab_name2 = tab.objectName()
            #     self.sub_tabs[tab_name1, tab_name2] = tab

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
            data_level = "Cell"
            column_value = self.cell_line_edit.text().strip()
        elif self.site_radio_btn.isChecked():
            data_level = "Site"
            column_value = self.site_line_edit.text().strip()

        elif self.cluster_radio_btn.isChecked():
            data_level = "Cluster"

        tab1 = self.tabwidget_level1.currentWidget()
        tab1_name = tab1.objectName()
        if tab1_name in CHARTS_TAB_NAMES:
            self.statusbar.showMessage("Loading Data from Server")
            for tech in ("2G", "4G", "5G"):
                if tech in tab1_name:
                    break

            if "Hourly" in tab1_name:
                time_level = "Hourly"
                time_col="Time"
                st = self.start_date_time_edit.dateTime().toPyDateTime()
                end = self.end_date_time_edit.dateTime().toPyDateTime()

            if "Daily" in tab1_name:
                time_level = "Daily"
                time_col="Date"
                st = self.start_date_edit.dateTime().toPyDateTime()
                end = self.end_date_edit.dateTime().toPyDateTime()

            # initiate sc
            project = set()
            config_df = self.charts_config.get(tab1_name, pd.DataFrame())
            if config_df.empty == False:
                #get data
                for tab2_name in config_df["Tab"].unique():
                    self.scrollaleChartsAreas[tab1_name, tab2_name].recreate()
                    # tab1.findChild(mpl_cls.ScrollaleChartsArea, tab2_name).recreate()
                for kpis in config_df["Kpis"]:
                    for kpi in kpis:
                        project.add(kpi)
                # print(project)

                data_collector = db_operator.Data_collector(MONGO_CLIENT_URL=self.MONGO_CLIENT_URL, tech=tech,
                                                            data_level=data_level, time_level=time_level,
                                                            agg_function=self.agg_function,
                                                            additional_kpi=self.additional_kpi,
                                                            conditional_kpi=self.conditional_kpi,
                                                            start_time=st, end_time=end, project=project,
                                                            key_values=[column_value], query_config=self.query_config,
                                                            )
                data_collector.query_data()
                # print(data_collector.final_df)
                if data_collector.final_df.empty:
                    self.show_error_message("No data for {}".format(column_value))
                    self.statusbar.showMessage("No data for {}".format(column_value))

                else:
                    # plot
                    # print(data_collector.final_df.columns.values)
                    for tab2_name in config_df["Tab"].unique():
                        tab_config_df=config_df[config_df["Tab"]==tab2_name]
                        sc=self.scrollaleChartsAreas[tab1_name,tab2_name]
                        sc.plot(tab_config_df,data_collector.final_df,data_level,column_value,time_col,self.small_legend_config)
                    self.statusbar.showMessage("Query finished")
            #
            #
            #
            # if query_level == "cell":
            #     column_name = "Cell Name"
            #     column_value = self.cell_line_edit.text().strip()
            #
            # if query_level == "site":
            #     if tab1_name.startswith("HUAWEI5G"):
            #         column_name = "gNodeB Name"  # todo need to consider 2/3/4G
            #         column_value = self.site_line_edit.text().strip()  # todo need to consider 2/3/4G
            # # todo cluster
            #
            # myclient = pymongo.MongoClient(MONGO_CLIENT_URL)
            # col = myclient[DB_NAME][collection_name]
            #
            # project[time_col] = 1
            # project[column_name] = 1
            # query = {column_name: column_value,
            #          time_col: {"$gte": st, "$lte": end}}
            # res = list(col.find(query, project))
            # if res:
            #     df = pd.DataFrame(res)
            #     df["GP"] = GP
            #     if query_level == "site":
            #         for kpi in set(agg):
            #             if kpi not in df.columns:
            #                 del agg[kpi]
            #                 print("missing {} in databse for {}".format(kpi, column_value))
            #         df = df.groupby([time_col, column_name], as_index=False).agg(agg)
            #
            #     for tab2_name in self.charts_config.get(tab1_name,{}):
            #         sc = tab1.findChild(mpl_cls.ScrollaleChartsArea, tab2_name)
            #         configs = self.charts_config[tab1_name][tab2_name]
            #         sc.plot(configs, df, GP, column_value, time_col,self.special_legend_title)
            #     self.statusbar.showMessage("{} {} query finished".format(column_value, tab1_name, 60000))
            # else:
            #     self.statusbar.showMessage("{} doesn't have data".format(column_value))
            #     # todo cluster
            # myclient.close()

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

    # autocomplete on cell line edit
    def on_cell_line_edit_textEdited(self, s):
        arr = []
        tab_name = self.tabwidget_level1.currentWidget().objectName()
        if tab_name in CHARTS_TAB_NAMES and len(s) >= 2:
            data_level = "Cell"
            row = self.auto_completer_Config.loc[tab_name, data_level]
            db_name, collection_name = row["db_name"], row["collection_name"]
            if pd.notnull(db_name) and pd.notnull(collection_name):
                mycol = self.mongo_client[db_name][collection_name]
                query = {"_id": re.compile("^{}".format(s), re.IGNORECASE)}
                arr = [d["_id"] for d in mycol.find(query, sort=[("_id", 1)])]
        self.cell_line_edit_autocompleter_model.clear()
        for text in arr:
            self.cell_line_edit_autocompleter_model.appendRow(QtGui.QStandardItem(text))

    # autocomplete on site line edit
    def on_site_line_edit_textEdited(self, s):
        arr = []
        tab_name = self.tabwidget_level1.currentWidget().objectName()
        if tab_name in CHARTS_TAB_NAMES and len(s) >= 2:
            data_level = "Site"
            row = self.auto_completer_Config.loc[tab_name, data_level]
            db_name, collection_name = row["db_name"], row["collection_name"]
            if pd.notnull(db_name) and pd.notnull(collection_name):
                mycol = self.mongo_client[db_name][collection_name]
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

    def show_error_message(self,s):
        em=QtWidgets.QErrorMessage(self)
        em.showMessage(s)


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
