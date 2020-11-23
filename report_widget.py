from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import traceback
import sys
from sort_and_filter_tbl_view import Sort_tbl_view
import pandas as pd
from mpl_cls import ScrollaleChartsArea
import os
import datetime
import numpy as np
import pandas.errors
import dateutil
from parameters import *
import pymongo
import db_operator


# class Report_scrollaleChartsArea(ScrollaleChartsArea):
#     def __init__(self,parent=None):
#         super(Report_scrollaleChartsArea,self).__init__(parent)
#
#     def add_charts(self):


class Report_widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Report_widget, self).__init__(parent)
        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.left_list = QtWidgets.QListWidget(self.splitter)
        self.left_list.addItem("Input")
        self.left_list.setObjectName(u"list_view")
        self.splitter.addWidget(self.left_list)
        self.stacked_widget = QtWidgets.QStackedWidget(self.splitter)
        self.stacked_widget.setObjectName(u"stacked_widget")
        self.input_page = QtWidgets.QWidget(self)
        self.input_page.setObjectName(u"input_page")
        self.input_report_btn = QtWidgets.QPushButton(parent=self.input_page, text="Load Report Input")
        self.export_single_site_btn = QtWidgets.QPushButton(parent=self.input_page, text="Export Single Site Report")
        self.export_all_site_btn = QtWidgets.QPushButton(parent=self.input_page, text="Export All Sites Reports")
        input_page_gridlayout = QtWidgets.QGridLayout(self.input_page)
        input_page_gridlayout.addWidget(self.input_report_btn, 0, 0)
        input_page_gridlayout.addWidget(self.export_single_site_btn, 0, 1)
        input_page_gridlayout.addWidget(self.export_all_site_btn, 0, 2)
        self.report_input_tbl = Sort_tbl_view(self.input_page)
        input_page_gridlayout.addWidget(self.report_input_tbl, 1, 0, 1, -1)
        self.input_page.setLayout(input_page_gridlayout)
        self.stacked_widget.addWidget(self.input_page)
        self.splitter.addWidget(self.stacked_widget)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.splitter)
        self.setLayout(layout)
        self.stacked_widgets = {}
        self.connect()

    def connect(self):
        self.left_list.currentRowChanged.connect(self.on_click_left_list_currentRowChanged)
        self.input_report_btn.clicked.connect(self.on_input_report_btn_clicked)
        self.export_single_site_btn.clicked.connect(self.on_export_single_site_btn_clicked)

    def set_input_page_df(self, df):
        self.report_input_tbl.set_df(df)
        # print(self.sites_list_tbl.)

    def on_click_left_list_currentRowChanged(self, i):
        self.stacked_widget.setCurrentIndex(i)

    def on_input_report_btn_clicked(self):
        fn = QtWidgets.QFileDialog.getOpenFileName(self, "Open ppo report input file", os.getcwd(), "*.xlsx")[0]
        if fn != "":
            valid, df = self.validate_report_input(fn)
            if valid:
                self.set_input_page_df(df)
            else:
                err = df
                QtWidgets.QErrorMessage(self).showMessage(err)

    def validate_report_input(self, fn):
        pass

    def on_export_single_site_btn_clicked(self):
        pass

    def on_export_all_site_btn_clicked(self):
        pass

    def add_tbl_tab(self, title, df):
        tbl_widget = Sort_tbl_view(self.stacked_widget)
        tbl_widget.set_df(df)
        self.left_list.addItem(title)
        self.stacked_widget.addWidget(tbl_widget)
        self.stacked_widgets[title] = tbl_widget

    def add_charts_tab(self):
        pass

    def clear_tabs(self):
        for title, w in self.stacked_widgets.items():
            print(title, w)
            list_widget = self.left_list.findItems(title, QtCore.Qt.MatchExactly)[0]
            self.left_list.takeItem(self.left_list.indexFromItem(list_widget).row())
            self.stacked_widget.removeWidget(w)
            w.deleteLater()
            del list_widget
        self.stacked_widgets = {}


class Ppo_report_widget(Report_widget):
    def __init__(self, config_df, query_config, agg_function, addtional_kpi, conditional_kpi, ignore_fields,
                 parent=None):
        super(Ppo_report_widget, self).__init__(parent=parent)
        self.config_df = config_df
        self.query_config = query_config
        self.agg_function = agg_function
        self.additional_kpi = addtional_kpi
        self.conditional_kpi = conditional_kpi
        self.ignore_fields = ignore_fields
        self.input_columns = {"DU ID": 'O', "Pre Start": 'datetime64[ns]', "Pre End": 'datetime64[ns]',
                              "Post Start": 'datetime64[ns]', "Post End": 'datetime64[ns]', "Days": 'int64',
                              "Day1": 'datetime64[ns]', "Day2": 'datetime64[ns]'}
        self.set_input_page_df(pd.DataFrame(columns=self.input_columns))

    def validate_report_input(self, fn):
        df = pd.read_excel(fn)
        if list(df.columns) != list(self.input_columns.keys()):
            err = "Wrong title, title must be the same."
            return False, err
        else:
            try:
                df = df.astype(self.input_columns)
                if df.isnull().values.any():
                    err = "empty values in input file"
                    return False, err
            except (dateutil.parser._parser.ParserError, ValueError) as e:
                print("values wrong in input file")
                print(type(e), e)
                err = "values wrong in input file"
                return False, err
            else:
                for ind, row in df.iterrows():
                    if not (datetime.datetime.today() - datetime.timedelta(days=row["Days"]) <= row[
                        "Day1"] <= datetime.datetime.today()) or not (
                            datetime.datetime.today() - datetime.timedelta(days=row["Days"]) <= row[
                        "Day2"] <= datetime.datetime.today()):
                        err = "row {} : Day1 or Day2 not in range".format(ind)
                        return False, err

                return True, df

    def on_export_single_site_btn_clicked(self):
        # todo
        df = self.report_input_tbl.model.df
        row = self.report_input_tbl.currentIndex().row()
        input_df = df.loc[row:row]
        self.query_sites_list(input_df)

    def query_sites_list(self, input_df):
        myclient = pymongo.MongoClient(MONGO_CLIENT_URL)
        mydb = myclient[EP_DB_NAME]
        mycol = mydb[ISDP_COL_NAME]
        missing_sites = []
        for index, row in input_df.iterrows():
            du_id = row["DU ID"]
            d = mycol.find_one({"_id": du_id})
            if d:
                sites_list = [d["Site ID"]]
                pre_st = row["Pre Start"]
                pre_end = row["Pre End"]
                days = row["Days"]
                post_st = row["Post Start"]
                post_end = row["Post End"]
                self.query_data(sites_list, pre_st, pre_end, days, post_st, post_end)
                print(self.gsm_site_level_pre_df)
                print(self.gsm_site_level_post_df)
                print(self.lte_site_level_pre_df)
                print(self.lte_site_level_post_df)
                print(self.lte_cell_level_pre_df)
                print(self.lte_cell_level_post_df)
            else:
                missing_sites.append(du_id)

    def query_data(self, sites_list, pre_st, pre_end, days, post_st, post_end):
        """
        2G/4G
        pre_site_level,post_site_level,pre_cell_level,post_site_level,
        """
        # create project
        project = set()
        for kpis in self.config_df["Kpis"]:
            for kpi in kpis:
                project.add(kpi)
        data_collector_2g_site_level_pre = db_operator.Data_collector(MONGO_CLIENT_URL=MONGO_CLIENT_URL, tech='2G',
                                                                      data_level="Site", time_level="Daily",
                                                                      agg_function=self.agg_function,
                                                                      additional_kpi=self.additional_kpi,
                                                                      conditional_kpi=self.conditional_kpi,
                                                                      start_time=pre_st, end_time=pre_end,
                                                                      project=project,
                                                                      key_values=sites_list,query_col="Site Name",
                                                                      query_config=self.query_config,
                                                                      layer=None, cluster=None,
                                                                      ignore_fields=self.ignore_fields, overall=True
                                                                      )
        data_collector_2g_site_level_pre.query_data()
        self.gsm_site_level_pre_df = data_collector_2g_site_level_pre.final_df
        data_collector_2g_site_level_post = db_operator.Data_collector(MONGO_CLIENT_URL=MONGO_CLIENT_URL, tech='2G',
                                                                       data_level="Site", time_level="Daily",
                                                                       agg_function=self.agg_function,
                                                                       additional_kpi=self.additional_kpi,
                                                                       conditional_kpi=self.conditional_kpi,
                                                                       start_time=post_st, end_time=post_end,
                                                                       project=project,
                                                                       key_values=sites_list,query_col="Site Name",
                                                                       query_config=self.query_config,
                                                                       layer=None, cluster=None,
                                                                       ignore_fields=self.ignore_fields, overall=True
                                                                       )
        data_collector_2g_site_level_post.query_data()
        self.gsm_site_level_post_df = data_collector_2g_site_level_post.final_df
        data_collector_4g_site_level_pre = db_operator.Data_collector(MONGO_CLIENT_URL=MONGO_CLIENT_URL, tech='4G',
                                                                      data_level="Site", time_level="Daily",
                                                                      agg_function=self.agg_function,
                                                                      additional_kpi=self.additional_kpi,
                                                                      conditional_kpi=self.conditional_kpi,
                                                                      start_time=pre_st, end_time=pre_end,
                                                                      project=project,
                                                                      key_values=sites_list,query_col="eNodeB Name",
                                                                      query_config=self.query_config,
                                                                      layer="All Site", cluster=None,
                                                                      ignore_fields=self.ignore_fields, overall=True
                                                                      )
        data_collector_4g_site_level_pre.query_data()
        self.lte_site_level_pre_df = data_collector_4g_site_level_pre.final_df
        data_collector_4g_site_level_post = db_operator.Data_collector(MONGO_CLIENT_URL=MONGO_CLIENT_URL, tech='4G',
                                                                       data_level="Site", time_level="Daily",
                                                                       agg_function=self.agg_function,
                                                                       additional_kpi=self.additional_kpi,
                                                                       conditional_kpi=self.conditional_kpi,
                                                                       start_time=post_st, end_time=post_end,
                                                                       project=project,
                                                                       key_values=sites_list,query_col="eNodeB Name",
                                                                       query_config=self.query_config,
                                                                       layer="All Site", cluster=None,
                                                                       ignore_fields=self.ignore_fields, overall=True
                                                                       )
        data_collector_4g_site_level_post.query_data()
        self.lte_site_level_post_df = data_collector_4g_site_level_post.final_df
        data_collector_4g_cell_level_pre = db_operator.Data_collector(MONGO_CLIENT_URL=MONGO_CLIENT_URL, tech='4G',
                                                                      data_level="Cell", time_level="Daily",
                                                                      agg_function=self.agg_function,
                                                                      additional_kpi=self.additional_kpi,
                                                                      conditional_kpi=self.conditional_kpi,
                                                                      start_time=pre_st, end_time=pre_end,
                                                                      project=project,
                                                                      key_values=sites_list,query_col="eNodeB Name",
                                                                      query_config=self.query_config,
                                                                      layer="All Site", cluster=None,
                                                                      ignore_fields=self.ignore_fields, overall=True
                                                                      )
        data_collector_4g_cell_level_pre.query_data()
        self.lte_cell_level_pre_df = data_collector_4g_cell_level_pre.final_df
        data_collector_4g_cell_level_post = db_operator.Data_collector(MONGO_CLIENT_URL=MONGO_CLIENT_URL, tech='4G',
                                                                       data_level="Cell", time_level="Daily",
                                                                       agg_function=self.agg_function,
                                                                       additional_kpi=self.additional_kpi,
                                                                       conditional_kpi=self.conditional_kpi,
                                                                       start_time=post_st, end_time=post_end,
                                                                       project=project,
                                                                       key_values=sites_list,query_col="eNodeB Name",
                                                                       query_config=self.query_config,
                                                                       layer="All Site", cluster=None,
                                                                       ignore_fields=self.ignore_fields, overall=True
                                                                       )
        data_collector_4g_cell_level_post.query_data()
        self.lte_cell_level_post_df = data_collector_4g_cell_level_post.final_df


if __name__ == "__main__":
    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("error catched!:")
        print("error message:\n", tb)
        QtWidgets.QApplication.quit()
        # or QtWidgets.QApplication.exit(0)


    sys.excepthook = excepthook
    app = QtWidgets.QApplication([])
    config_df = pd.read_excel("template.xlsx", sheet_name="ppo_config")
    myWin = Ppo_report_widget()
    myWin.show()
    sys.exit(app.exec_())
