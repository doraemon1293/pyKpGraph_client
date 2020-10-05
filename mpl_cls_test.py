import matplotlib
import sys
import matplotlib.ticker as mtick
import math
import copy

matplotlib.use('Qt5Agg')
import numpy as np
import traceback
from PyQt5 import QtWidgets
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import db_operator
import datetime
import pandas as pd
import openpyxl
import util
from mpl_cls import *
import math

pd.options.display.max_columns = None
pd.options.display.max_rows = None


class My_test_main_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(My_test_main_window, self).__init__(None)
        self.load_config("template_test.xlsx")
        dr = pd.date_range(start=datetime.datetime(2020, 7, 23),
                           end=datetime.datetime(2020, 7, 23, 12, 0), freq="H")
        self.data_df = pd.DataFrame({"Cell Name": ["cell1"] * len(dr),
                                     "Date": dr,
                                     "A": [math.sin(x) for x in range(1, len(dr) + 1)],
                                     "B": [x * 2 for x in range(1, len(dr) + 1)],
                                     "stack1": [x for x in range(1, len(dr) + 1)],
                                     "stack2": [2 * x for x in range(1, len(dr) + 1)],
                                     "stack3": [3 * x for x in range(1, len(dr) + 1)],
                                     "group1": [x for x in range(1, len(dr) + 1)],
                                     "group2": [2 * x for x in range(1, len(dr) + 1)],
                                     "group3": [3 * x for x in range(1, len(dr) + 1)],
                                     "group4": [4 * x for x in range(1, len(dr) + 1)],
                                     "group5": [5 * x for x in range(1, len(dr) + 1)],
                                     "group6": [6 * x for x in range(1, len(dr) + 1)],

                                     }
                                    )

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
            if ws.title == "test_plot_config":
                df = pd.read_excel(filename, sheet_name=ws.title)
                df = df.apply(util.compile_formula_in_df, axis=1)
                self.charts_config = df

            # if ws.title == "small_legend_config":
            #     df = pd.read_excel(filename, sheet_name=ws.title)
            #     self.small_legend_config = {}
            #     for _, row in df.iterrows():
            #         self.small_legend_config[row["Parameter"]] = row["Value"]
            #     # self.small_legend_config["bbox_to_anchor"] = eval(self.small_legend_config["bbox_to_anchor"])
            #     # self.small_legend_config["ncol"] = int(self.small_legend_config["ncol"])
            #     self.small_legend_config["fontsize"] = str(self.small_legend_config["fontsize"])

    # def gen_df(self):
    #     project={'N_RA_Dedicated_Msg3', 'N_ThpTime_UE_UL_RmvSmallPkt(microsecond)', 'N_DL_Pwr_Max(dBm)',
    #     'N_ThpVol_DL_Cell(kbit)', 'N_PRB_UL_Avail_Avg', 'N_User_RRCConn_Active_UL_Avg', 'N_CCE_Avail_Avg',
    #     'N_PRB_UL_Used_Avg', 'N_ThpVol_UL(kbit)', 'N_Cell_Unavail_Dur_System(s)', 'N_User_RRCConn_Active_UL_Max',
    #     'N_NsaDc_IntraSgNB_PSCell_Change_Att', 'N_NsaDc_IntraSgNB_PSCell_Change_Succ', 'N_User_RRCConn_Active_Avg',
    #     'N_UL_RSSI_Min(dBm)', 'N_NsaDc_DRB_Rel', 'N_ThpVol_DL(kbit)', 'N_User_RRCConn_Active_Max',
    #     'N_PRB_DL_Used_Avg', 'N_ThpVol_DL_LastSlot(kbit)', 'N_NsaDc_InterSgNB_PSCell_Change_Succ',
    #     'N_ThpTime_DL_Cell(microsecond)', 'N_Cell_Unavail_Dur_Manual(s)', 'N_UL_RSSI_Avg(dBm)',
    #     'N_NsaDc_DRB_Add_Succ', 'N_PRB_DL_Avail_Avg', 'N_NsaDc_DRB_AbnormRel', 'N_DL_AvgPrdPwr_Max(dBm)',
    #     'N_User_NsaDc_PSCell_Avg', 'N_User_RRCConn_Active_DL_Max', 'N_NsaDc_SgNB_Rel', 'N_ThpVol_UE_UL_SmallPkt(
    #     kbit)', 'N_UL_NI_Max(dBm)', 'N_UL_NI_Min(dBm)', 'N_UL_NI_Avg(dBm)', 'N_NsaDc_DRB_Add_Att',
    #     'N_RA_Dedicated_Att', 'N_ThpTime_DL_RmvLastSlot(microsecond)', 'N_NsaDc_InterSgNB_PSCell_Change_Att',
    #     'N_ThpVol_UL_Cell(kbit)', 'N_NsaDc_SgNB_Add_Att', 'GP', 'N_CCE_Used_Avg', 'N_NsaDc_SgNB_AbnormRel',
    #     'N_User_RRCConn_Active_DL_Avg', 'N_NsaDc_SgNB_Add_Succ', 'N_User_RRCConn_Max',
    #     'N_NsaDc_SgNB_AbnormRel_Radio', 'N_User_RRCConn_Avg', 'N_ThpTime_UL_Cell(microsecond)'}
    #
    #     column_value=["15474NBn781"]
    #     data_collector = db_operator.Data_collector(MONGO_CLIENT_URL=self.MONGO_CLIENT_URL, tech="5G",
    #                                                 data_level="Cell", time_level="Hourly",
    #                                                 agg_function=self.agg_function,
    #                                                 additional_kpi=self.additional_kpi,
    #                                                 conditional_kpi=self.conditional_kpi,
    #                                                 start_time=datetime.datetime(2020,7,23),
    #                                                 end_time=datetime.datetime(2020,7,24), project=project,
    #                                                 key_values=column_value, query_config=self.query_config,
    #                                                 )
    #     return data_collector.query_data()
    #


if __name__ == "__main__":
    sys._excepthook = sys.excepthook


    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook

    app = QtWidgets.QApplication(sys.argv)
    my_test_main_window = My_test_main_window()
    sc = ScrollaleChartsArea(my_test_main_window)
    my_test_main_window.setCentralWidget(sc)
    my_test_main_window.show()
    sc.plot(my_test_main_window.charts_config, my_test_main_window.data_df, data_level="Cell",column_value="lalala",
            time_col="Date")
    sys.exit(app.exec_())
