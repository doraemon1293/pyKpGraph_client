import sys
import traceback
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, QSortFilterProxyModel, QMetaObject, QObject
import PyQt5.QtCore as QtCore
from PyQt5 import uic
import datetime
from sort_and_filter_tbl_view import Sort_tbl_view
from numpy import log10
import pickle

# from ui_table_tab import Ui_Table_tab
# Ui_Table_tab,_=uic.loadUiType("table_tab.ui")
class General_table(QtWidgets.QWidget):
    def __init__(self, config_df, tab_name="", start_time="", end_time="", object_name="", parent=None,
                 df=pd.DataFrame(), ):
        super(General_table, self).__init__(parent)
        # self.setupUi(self)
        self.tab_name = tab_name
        self.object_label = QtWidgets.QLabel(self)
        self.object_label.setText("Object: {}".format(object_name))
        self.date_range_label = QtWidgets.QLabel(self)
        if type(start_time) == datetime.datetime:
            start_time = start_time.strftime("%d.%m.%Y")
        if type(end_time) == datetime.datetime:
            end_time = end_time.strftime("%d.%m.%Y")
        self.date_range_label.setText("Average From: {} To: {}".format(start_time, end_time))
        self.checkBox_day_by_day = QtWidgets.QCheckBox(self, text="Day By Day")
        self.checkBox_day_by_day.setChecked(True)
        self.export_to_csv_btn = QtWidgets.QPushButton(self, text="Export to CSV")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.addWidget(self.object_label)
        self.horizontalLayout.addWidget(self.date_range_label)
        self.horizontalLayout.addWidget(self.checkBox_day_by_day)
        self.horizontalLayout.addWidget(self.export_to_csv_btn)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table_view = Sort_tbl_view(self)
        self.verticalLayout.addWidget(self.table_view)

        self.config_df = config_df
        self.ori_df = df

        self.connect()

    def set_title(self, start_time="", end_time="", object_name="", agg_function={}):
        self.object_label.setText("Object: {}".format(object_name))
        if type(start_time) == datetime.datetime:
            start_time = start_time.strftime("%d.%m.%Y")
        if type(end_time) == datetime.datetime:
            end_time = end_time.strftime("%d.%m.%Y")
        self.date_range_label.setText("Average From: {} To: {}".format(start_time, end_time))

    def set_df(self, df, agg_function):
        self.ori_df = df
        self.agg_function = agg_function
        self.day_by_day_df = pd.DataFrame()
        if df.empty == False:
            config_df = self.config_df[self.config_df["Day_by_day"] == False]
            for index, row in config_df.iterrows():
                self.day_by_day_df[row["Kpi_name"]] = eval(row["Formula"])
        self.agg_df = self.agg()
        self.on_checkBox_day_by_day_stateChanged()

    def connect(self):
        self.checkBox_day_by_day.stateChanged.connect(self.on_checkBox_day_by_day_stateChanged)

    def on_checkBox_day_by_day_stateChanged(self):
        if self.ori_df.empty:
            self.table_view.set_df(self.ori_df)
        else:
            if self.checkBox_day_by_day.isChecked():
                self.table_view.set_df(self.day_by_day_df)
            else:
                self.table_view.set_df(self.agg_df)

    def agg(self):
        if self.ori_df.empty == False:
            if self.tab_name == "TRX":
                grouby_columns = ["Cell Name", "TRXNo", "TRXIndex", "GBSC", "Site Name"]

            if self.tab_name == "2G HO/NB":
                grouby_columns = ["Cell Name", "Cell CI", "GBSC", "Target BSC Name", "Target Cell Name", "Target CI",
                                  "Cell LAC", "Target LAC"]
            if self.tab_name == "4G Intra HO/NB":
                grouby_columns = ['Cell Name', 'eNodeB Name', 'Local cell identity', 'Target Cell Name',
                                  'Target eNodeB ID', 'Target Cell ID']
            if self.tab_name == "IRAT 2G HO/NB":
                grouby_columns = ['Cell Name', 'Target cell ID', 'Target Cell Name', 'eNodeB Name', 'Local cell ID',
                                  'Target LAC', 'Target MCC', 'Target MNC']
            if self.tab_name == "IRAT 3G HO/NB":
                grouby_columns = ['Cell Name','Target cell ID','eNodeB Name','Local cell ID','Target RNC ID','Target MCC','Target MNC']

            agg_dict = {}
            for col in self.ori_df.columns:
                if col not in grouby_columns:
                    if col in self.agg_function:
                        agg_dict[col] = self.agg_function[col]
                    else:
                        agg_dict[col] = lambda x: x.sum(min_count=1)
            agg_dict["Date"] = "count"
            df = self.ori_df.groupby(grouby_columns, as_index=False,dropna=False).agg(agg_dict)
            df.rename(columns={"Date": "Days"}, inplace=True)
            agg_df = pd.DataFrame()
            config_df = self.config_df[self.config_df["Day_by_day"] == True]
            for index, row in config_df.iterrows():
                agg_df[row["Kpi_name"]] = eval(row["Formula"])
            agg_df.rename(columns={"Date": "Days"}, inplace=True)
            # if self.tab_name == "IRAT 2G HO/NB":
            #     print(df)
            #     print(self.ori_df.columns, self.ori_df.shape)
            #     print(agg_df.shape, agg_df.columns)
            #     pickle.dump(self.ori_df,open("1.tmp","wb"))
            return agg_df
        else:
            return self.ori_df


# class General_table(QtWidgets.QWidget):
#     def __init__(self, config_df, tab_name="", start_time="", end_time="", object_name="", parent=None,
#                  df=pd.DataFrame(), ):
#         super(General_table, self).__init__(parent)
#         # self.setupUi(self)
#         self.tab_name = tab_name
#         self.object_label = QtWidgets.QLabel(self)
#         self.object_label.setText("Object: {}".format(object_name))
#         self.date_range_label = QtWidgets.QLabel(self)
#         if type(start_time) == datetime.datetime:
#             start_time = start_time.strftime("%d.%m.%Y")
#         if type(end_time) == datetime.datetime:
#             end_time = end_time.strftime("%d.%m.%Y")
#         self.date_range_label.setText("Average From: {} To: {}".format(start_time, end_time))
#         self.checkBox_day_by_day = QtWidgets.QCheckBox(self, text="Day By Day")
#         self.checkBox_day_by_day.setChecked(True)
#         self.export_to_csv_btn = QtWidgets.QPushButton(self, text="Export to CSV")
#
#         self.horizontalLayout = QtWidgets.QHBoxLayout()
#         self.horizontalLayout.addWidget(self.object_label)
#         self.horizontalLayout.addWidget(self.date_range_label)
#         self.horizontalLayout.addWidget(self.checkBox_day_by_day)
#         self.horizontalLayout.addWidget(self.export_to_csv_btn)
#         self.verticalLayout = QtWidgets.QVBoxLayout(self)
#         self.verticalLayout.addLayout(self.horizontalLayout)
#         self.table_view = Sort_and_filter_tbl_view(self)
#         self.verticalLayout.addWidget(self.table_view)
#
#         self.config_df = config_df
#         self.ori_df = df
#
#         self.connect()
#
#     def set_title(self, start_time="", end_time="", object_name="", agg_function={}):
#         self.object_label.setText("Object: {}".format(object_name))
#         if type(start_time) == datetime.datetime:
#             start_time = start_time.strftime("%d.%m.%Y")
#         if type(end_time) == datetime.datetime:
#             end_time = end_time.strftime("%d.%m.%Y")
#         self.date_range_label.setText("Average From: {} To: {}".format(start_time, end_time))
#
#     def set_df(self, df, agg_function):
#         self.ori_df = df
#         self.agg_function = agg_function
#         self.day_by_day_df = pd.DataFrame()
#         if df.empty == False:
#             config_df = self.config_df[self.config_df["Day_by_day"] == False]
#             for index, row in config_df.iterrows():
#                 self.day_by_day_df[row["Kpi_name"]] = eval(row["Formula"])
#         self.agg_df = self.agg()
#         self.on_checkBox_day_by_day_stateChanged()
#
#     def connect(self):
#         self.checkBox_day_by_day.stateChanged.connect(self.on_checkBox_day_by_day_stateChanged)
#
#     def on_checkBox_day_by_day_stateChanged(self):
#         if self.ori_df.empty:
#             self.table_view.set_df(self.ori_df)
#         else:
#             if self.checkBox_day_by_day.isChecked():
#                 self.table_view.set_df(self.day_by_day_df)
#             else:
#                 self.table_view.set_df(self.agg_df)
#
#     def agg(self):
#         if self.ori_df.empty == False:
#             if self.tab_name == "TRX":
#                 grouby_columns = ["Cell Name", "TRXNo", "TRXIndex", "GBSC", "Site Name"]
#
#             if self.tab_name == "2G HO/NB":
#                 grouby_columns = ["Cell Name", "Cell CI", "GBSC", "Target BSC Name", "Target Cell Name", "Target CI",
#                                   "Cell LAC", "Target LAC"]
#             if self.tab_name == "4G Intra HO/NB":
#                 grouby_columns = ['Cell Name', 'eNodeB Name', 'Local cell identity', 'Target Cell Name',
#                                   'Target eNodeB ID', 'Target Cell ID']
#             if self.tab_name == "IRAT 2G HO/NB":
#                 grouby_columns = ['Cell Name', 'Target cell ID', 'Target Cell Name', 'eNodeB Name', 'Local cell ID',
#                                   'Target LAC', 'Target MCC', 'Target MNC']
#             if self.tab_name == "IRAT 3G HO/NB":
#                 grouby_columns = ['Cell Name','Target cell ID','eNodeB Name','Local cell ID','Target RNC ID','Target MCC','Target MNC']
#
#             agg_dict = {}
#             for col in self.ori_df.columns:
#                 if col not in grouby_columns:
#                     if col in self.agg_function:
#                         agg_dict[col] = self.agg_function[col]
#                     else:
#                         agg_dict[col] = lambda x: x.sum(min_count=1)
#             agg_dict["Date"] = "count"
#             df = self.ori_df.groupby(grouby_columns, as_index=False,dropna=False).agg(agg_dict)
#             df.rename(columns={"Date": "Days"}, inplace=True)
#             agg_df = pd.DataFrame()
#             config_df = self.config_df[self.config_df["Day_by_day"] == True]
#             for index, row in config_df.iterrows():
#                 agg_df[row["Kpi_name"]] = eval(row["Formula"])
#             agg_df.rename(columns={"Date": "Days"}, inplace=True)
#             # if self.tab_name == "IRAT 2G HO/NB":
#             #     print(df)
#             #     print(self.ori_df.columns, self.ori_df.shape)
#             #     print(agg_df.shape, agg_df.columns)
#             #     pickle.dump(self.ori_df,open("1.tmp","wb"))
#             return agg_df
#         else:
#             return self.ori_df




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    o = General_table(pd.DataFrame())
    o.set_title("start", "endend",
                "objetc___1111111111111111111111111111111111111111111111111111111111111111111111_name")
    o.show()
    app.exec_()
