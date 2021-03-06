import sys
import traceback
import openpyxl
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import mpl_cls
import pymongo
import util
import pandas as pd
import os
import db_operator
from cluster_definition_widget import Cluster_definition_widget
from ui_mainwindow import Ui_MainWindow
from list_view import ListDialog
from table_cls import General_table
from parameters import *
import report_widget

pd.options.display.max_columns = None
pd.options.display.max_rows = None


# Ui_MainWindow, QtBaseClass = uic.loadUiType("Mainwindow.ui")

class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(MyMainWindow, self).__init__(parent)
        self.not_init = True
        self.MONGO_CLIENT_URL = MONGO_CLIENT_URL
        self.reload_template_file("template.xlsx")
        self.pre_load()

        self.start_date_time_edit.setDateTime(QtCore.QDateTime.fromString('2020/7/23 00:00:00', 'yyyy/M/d hh:mm:ss'))
        self.end_date_time_edit.setDateTime(QtCore.QDateTime.fromString('2020/7/24 00:00:00', 'yyyy/M/d hh:mm:ss'))
        self.start_date_edit.setDateTime(QtCore.QDateTime.fromString('2020/7/23', 'yyyy/M/d'))
        self.end_date_edit.setDateTime(QtCore.QDateTime.fromString('2020/7/29', 'yyyy/M/d'))
        self.tabwidget_level1.setCurrentIndex(1)
        self.cell_line_edit.setText("12330A80")
        self.site_line_edit.setText("12330")

    # def setupUi_2(self):

    def pre_load(self):
        myclient = pymongo.MongoClient(MONGO_CLIENT_URL)
        mydb = myclient[EP_DB_NAME]
        mycol = mydb[CLUTSER_COL_NAME]
        # load cluster definition
        self.cluster_def = pd.DataFrame(list(mycol.find({}, {"_id": 0})))
        self.cluster_def.sort_index(axis=1, inplace=True)
        self.cluster_combo_box.clear()
        self.cluster_combo_box.addItems(sorted(self.cluster_def["Cluster"].unique()))

        self.date_changed_lines = []

        # load auto_complete values
        self.auto_completer_dict = {}
        for _, row in self.auto_completer_Config.iterrows():
            self.auto_completer_dict[row["tab_name"], row["agg_level"]] = set(
                [d["_id"] for d in myclient[row["db_name"]][row["collection_name"]].find()])
        myclient.close()

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
        self.cell_line_edit_autocompleter_model = QtCore.QStringListModel()
        self.cell_line_edit_autocompleter.setModel(self.cell_line_edit_autocompleter_model)
        self.cell_line_edit.setCompleter(self.cell_line_edit_autocompleter)

        self.site_line_edit_autocompleter = QtWidgets.QCompleter()
        self.site_line_edit_autocompleter_model = QtCore.QStringListModel()
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
        self.scrollaleChartsAreas = {}
        self.table_tabs = {}
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
        self.table_tabs_config = {}
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
            if ws.title == "query_config":
                self.query_config = pd.read_excel(filename, sheet_name=ws.title)
            if ws.title == "table_tabs_config":
                df = pd.read_excel(filename, sheet_name=ws.title)
                df = df.apply(util.compile_formula_in_df, axis=1)
                for tab1_name in df["Parent_tab"].unique():
                    self.table_tabs_config[tab1_name] = df[df["Parent_tab"] == tab1_name]
            if ws.title == "ignore_fields":
                df = pd.read_excel(filename, sheet_name=ws.title)
                self.ignore_fields = set(df["Ignore_fields"])
            if ws.title == "ppo_config":
                df = pd.read_excel(filename, sheet_name=ws.title)
                df = df.apply(util.compile_formula_in_df, axis=1)
                self.ppo_config = df

    def build_tab_widgets(self):
        '''
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
            config_df = self.table_tabs_config.get(tab_name1, pd.DataFrame())
            if config_df.empty == False:
                for tab_name2 in config_df["Tab"].unique():
                    df = config_df[config_df["Tab"] == tab_name2]
                    tab2 = General_table(df, parent=tab1, tab_name=tab_name2)
                    tab2.setObjectName(tab_name2)
                    tab1.insertTab(ind, tab2, tab_name2)
                    ind += 1
                    self.table_tabs[tab_name1, tab_name2] = tab2
        self.ppo_report_widget = report_widget.Ppo_report_widget(self.ppo_config, self.query_config, self.agg_function,
                                                                 self.additional_kpi, self.conditional_kpi,
                                                                 self.ignore_fields)
        self.report.clear()
        self.report.insertTab(0,self.ppo_report_widget, "PPO Report")

    def connect(self):
        self.actionExport_All_CHarts_to_Excel.triggered.connect(self.export_all_charts_to_excel)
        self.actionReload_Template.triggered.connect(self.reload_template_file)
        self.actionCluster_Definition.triggered.connect(self.show_cluster_definition_widget)
        self.actionChange_Date_Line.triggered.connect(self.show_change_date_line_widget)
        self.query_push_btn.clicked.connect(self.on_query_push_btn_clicked)
        self.tabwidget_level1.currentChanged.connect(self.on_tabwidget_level1_currentChanged)
        self.cell_line_edit.textEdited.connect(self.on_cell_line_edit_textEdited)
        self.site_line_edit.textEdited.connect(self.on_site_line_edit_textEdited)
        self.site_line_edit.textChanged.connect(self.on_site_line_edit_textChanged)

    # QtCore.QMetaObject.connectSlotsByName(self)

    def show_cluster_definition_widget(self):
        cluster_definition_widget = Cluster_definition_widget(df=self.cluster_def, mongo_client=self.mongo_client,
                                                              EP_DB_NAME=EP_DB_NAME,
                                                              CLUTSER_COL_NAME=CLUTSER_COL_NAME,
                                                              parent=self)
        cluster_definition_widget.exec_()
        if cluster_definition_widget.result() == QtWidgets.QDialog.Accepted:
            self.cluster_def = cluster_definition_widget.cluster_tbl_view.model.df
            self.cluster_combo_box.clear()
            self.cluster_combo_box.addItems(sorted(self.cluster_def["Cluster"].unique()))

    def show_change_date_line_widget(self):
        date_changed_lines_dialog = ListDialog(type_="Date", arr=self.date_changed_lines, title="Set Change Date Line")
        date_changed_lines_dialog.exec_()
        if date_changed_lines_dialog.result() == QtWidgets.QDialog.Accepted:
            self.date_changed_lines = date_changed_lines_dialog.model.arr

    def export_all_charts_to_excel(self):
        print("todo")

    def clear_sc(self):
        for sc in self.scrollaleChartsAreas.values():
            sc.recreate()

    def on_query_push_btn_clicked(self):
        print("query_push_btn clicked")
        tab1 = self.tabwidget_level1.currentWidget()
        tab1_name = tab1.objectName()
        if tab1_name in CHARTS_TAB_NAMES:
            self.statusbar.showMessage("Loading Data from Server")
            self.statusbar.repaint()
            for tech in ("2G", "4G", "5G"):
                if tech in tab1_name:
                    break

            if self.cell_radio_btn.isChecked():
                agg_level = "Cell"
                column_value = self.cell_line_edit.text().strip()
                key_values = [column_value]
                query_col = "Cell Name"
            elif self.site_radio_btn.isChecked():
                agg_level = "Site"
                column_value = self.site_line_edit.text().strip()
                key_values = [column_value]
                if tech == "2G":
                    query_col = "Site Name"
                elif tech == "4G":
                    query_col = "eNodeB Name"
                elif tech == "5G":
                    query_col = "gNodeB Name"
            elif self.cluster_radio_btn.isChecked():
                agg_level = "Cluster"
                column_value = self.cluster_combo_box.currentText()
                if tech == "2G":
                    query_col = "Site Name"
                elif tech == "4G":
                    query_col = "eNodeB Name"
                elif tech == "5G":
                    query_col = "gNodeB Name"

            if agg_level == "Cluster":
                if tech in ("2G", "4G"):
                    key_values = list(set(self.cluster_def[self.cluster_def["Cluster"] == column_value]["Site"]))
                elif tech == "5G":
                    key_values = list(set(
                        [site + "N" for site in self.cluster_def[self.cluster_def["Cluster"] == column_value]["Site"]]))
            else:
                key_values == [column_value]

            if "Hourly" in tab1_name:
                time_level = "Hourly"
                time_col = "Time"
                st = self.start_date_time_edit.dateTime().toPyDateTime()
                end = self.end_date_time_edit.dateTime().toPyDateTime()

            if "Daily" in tab1_name:
                time_level = "Daily"
                time_col = "Date"
                st = self.start_date_edit.dateTime().toPyDateTime()
                end = self.end_date_edit.dateTime().toPyDateTime()

            # initiate sc
            project = set()
            charts_config_df = self.charts_config.get(tab1_name, pd.DataFrame())
            tbl_tab_config_df = self.table_tabs_config.get(tab1_name, pd.DataFrame())
            if charts_config_df.empty == False:
                # get data
                # get projection - all required fields
                for tab2_name in charts_config_df["Tab"].unique():
                    self.scrollaleChartsAreas[tab1_name, tab2_name].recreate()
                # get projection for charts
                for kpis in charts_config_df["Kpis"]:
                    for kpi in kpis:
                        project.add(kpi)
                # get projection for table tab
                if tbl_tab_config_df.empty == False:
                    for kpis in tbl_tab_config_df["Kpis"]:
                        for kpi in kpis:
                            project.add(kpi)
                layer = None
                if tech == "4G":
                    layer = self.layer_combo_box.currentText()
                data_collector = db_operator.Data_collector(MONGO_CLIENT_URL=self.MONGO_CLIENT_URL, tech=tech,
                                                            agg_level=agg_level, time_level=time_level,
                                                            agg_function=self.agg_function,
                                                            additional_kpi=self.additional_kpi,
                                                            conditional_kpi=self.conditional_kpi,
                                                            start_time=st, end_time=end, project=project,
                                                            key_values=key_values, query_col=query_col,
                                                            query_config=self.query_config,
                                                            layer=layer, cluster=column_value,
                                                            ignore_fields=self.ignore_fields,
                                                            )
                data_collector.query_chart_data()
                ori_dfs = data_collector.raw_dfs
                chart_data_df = data_collector.final_df
                trx_df = ori_dfs.get("trx_df", None)
                eth_df = ori_dfs.get("eth_df", None)
                if chart_data_df.empty:
                    self.show_error_message("No data for {}".format(column_value))
                    self.statusbar.showMessage("No data for {}".format(column_value))
                else:
                    # plot
                    for tab2_name in charts_config_df["Tab"].unique():
                        tab_config_df = charts_config_df[charts_config_df["Tab"] == tab2_name]
                        sc = self.scrollaleChartsAreas[tab1_name, tab2_name]
                        sc.plot(tab_config_df, chart_data_df, agg_level, column_value, time_col, trx_df, eth_df, layer,
                                self.date_changed_lines)
                    self.statusbar.showMessage("Query finished")
                if tbl_tab_config_df.empty == False:
                    for tab2_name in tbl_tab_config_df["Tab"].unique():
                        config_df = tbl_tab_config_df[tbl_tab_config_df["Tab"] == tab2_name]
                        df_name = config_df["Df_name"].unique()[0]
                        table_tab = self.table_tabs[tab1_name, tab2_name]
                        table_tab.set_title(start_time=st, end_time=end, object_name=column_value)
                        table_tab.set_df(ori_dfs.get(df_name, pd.DataFrame()), agg_function=self.agg_function)

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
        if "4G" in tab_name and len(self.site_line_edit.text()) == 5:
            self.layer_combo_box.setEnabled(True)
        else:
            self.layer_combo_box.setEnabled(False)

    # autocomplete on cell line edit
    def on_cell_line_edit_textEdited(self, s):
        arr = []
        tab_name = self.tabwidget_level1.currentWidget().objectName()
        if tab_name in CHARTS_TAB_NAMES and len(s) >= AUTO_COMPLETE_LENGTH:
            agg_level = "Cell"
            arr = sorted([x for x in self.auto_completer_dict[tab_name, agg_level] if x.startswith(s)])
        self.cell_line_edit_autocompleter_model.setStringList(arr)

    # autocomplete on site line edit
    def on_site_line_edit_textEdited(self, s):
        arr = []
        tab_name = self.tabwidget_level1.currentWidget().objectName()
        if tab_name in CHARTS_TAB_NAMES and AUTO_COMPLETE_LENGTH <= len(s) <= 20:
            agg_level = "Site"
            arr = sorted([x for x in self.auto_completer_dict[tab_name, agg_level] if x.startswith(s)])
        self.site_line_edit_autocompleter_model.setStringList(arr)

    def on_site_line_edit_textChanged(self, s):
        tab_name = self.tabwidget_level1.currentWidget().objectName()
        if tab_name in CHARTS_TAB_NAMES and "4G" in tab_name and len(s) == 5:
            mycol = self.mongo_client[EP_DB_NAME][LTE_EP_COL_NAME]
            query = {"eNodeB Name": s}
            arr = sorted(set([d["layer"] for d in mycol.find(query) if pd.notnull(d["layer"])] + ["All Site"]))
            self.layer_combo_box.setEnabled(True)
            self.layer_combo_box.clear()
            self.layer_combo_box.addItems(arr)
            self.layer_combo_box.setCurrentText("All Site")
        else:
            self.layer_combo_box.setEnabled(False)

    def contextMenuEvent(self, event):
        contextMenu = QtWidgets.QMenu(self)
        export_all_charts_act = contextMenu.addAction("Export All to Excel")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        # if action == quitAct:
        #     self.close()

    def closeEvent(self, event):
        self.mongo_client.close()

    def show_error_message(self, s):
        em = QtWidgets.QErrorMessage(self)
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
