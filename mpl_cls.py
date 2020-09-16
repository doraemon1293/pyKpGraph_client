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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg#, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import db_operator
import datetime
import pandas as pd
import openpyxl
import util
import special_plot

CHARTS_TAB_NAMES = {"HUAWEI2G_Hourly_tab", "HUAWEI2G_Daily_tab", "HUAWEI4G_Hourly_tab", "HUAWEI4G_Daily_tab",
                    "HUAWEI5G_Hourly_tab", "HUAWEI5G_Daily_tab"}
MONGO_CLIENT_URL = "mongodb://localhost:27017/"

GENERAL_LEGEND_CONFIG_LEFT = {"loc": "upper left", "bbox_to_anchor": (-0.15, 1.15), "frameon": False,
                              "fontsize": "small"}
GENERAL_LEGEND_CONFIG_RIGHT = {"loc": "upper right", "bbox_to_anchor": (1, 1.15), "frameon": False, "fontsize": "small"}



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, dpi=100):
        self.fig = Figure(dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)


class MplWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(MplWidget, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.canvas = MplCanvas(parent=self, dpi=dpi)
        self.toolbar = NavigationToolbar(self.canvas, self, None)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)


class ScrollaleChartsArea(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super(ScrollaleChartsArea, self).__init__(parent=parent)
        self.setWidgetResizable(True)
        self.recreate()

    def recreate(self):
        if hasattr(self, "scroll_widget"):
            self.scroll_widget.deleteLater()
        self.scroll_widget = QtWidgets.QWidget(self)
        self.gridlayout = QtWidgets.QGridLayout(self.scroll_widget)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setContentsMargins(0, 0, 0, 0)
        self.scroll_widget.setLayout(self.gridlayout)
        self.setWidget(self.scroll_widget)
        self.axes = {}
        self.widgets = {}

    def pre_plot(self):
        self.widget = MplWidget(parent=self.scroll_widget)
        self.widgets[self.chart_no] = self.widget
        self.config = self.config_df[self.config_df["Chart_no"] == self.chart_no]
        if "Special_chart" in self.config.columns and pd.notnull(self.config["Special_chart"].unique()[0]):
            self.special_chart = True
            self.function_name=self.config["Special_chart"].unique()[0]
        else:
            self.special_chart = False
        if "Small_legend" in self.config.columns and self.config["Small_legend"].unique()[0] == True:
            self.small_legend = True
        else:
            self.small_legend = False
        if self.time_col=="Time" or "Wide_chart" in self.config.columns and self.config["Wide_chart"].unique()[0] == True:
            width_chart = True
        else:
            width_chart = False
        if "Overall_chart" in self.config.columns and self.config["Overall_chart"].unique()[0] == True:
            self.overall_chart = True
        else:
            self.overall_chart = False
        if "Not_for_cell_level" in self.config.columns and self.config["Not_for_cell_level"].unique()[0] == True:
            self.not_for_cell_level = True
        else:
            self.not_for_cell_level = False


        self.title = self.config["Chart_tile"].unique()[0]

        rect = QtWidgets.QApplication.desktop().screenGeometry()
        height = rect.height() // 2 - 50

        if width_chart:
            width = rect.width() - 100
            if self.grid_column==1:
                self.grid_row+=1
                self.grid_column=0
            self.gridlayout.addWidget(self.widget, self.grid_row,self.grid_column,1,2)
            self.grid_row+=1
            self.grid_column=0
        else:
            width = rect.width() // 2 - 50
            self.gridlayout.addWidget(self.widget, self.grid_row,self.grid_column)
            self.grid_column+=1
            if self.grid_column==2:
                self.grid_row+=1
                self.grid_column=0
        self.widget.setFixedWidth(width)
        self.widget.setFixedHeight(height)
        self.ax1 = self.widget.canvas.fig.add_subplot(111)
        self.ax1.set_title("{} , {}".format(self.title, self.column_value))
        if self.not_for_cell_level and self.data_level=="Cell":
            self.ax1.set_title("{} , {}".format(self.title, "Not for cell level"))
            return False

        self.ax1.grid(axis='y')
        self.ax1.set_axisbelow(True)
        self.left_count = len(self.config[self.config["Axis"] == "Left"])
        self.right_count = len(self.config[self.config["Axis"] == "Right"])
        self.bottom = 0
        self.group_bar_no = self.config[self.config["Chart_type"] == "GroupBar"].shape[0]
        self.bar_width = 0.8 if self.time_col == "Date" else 0.8 / 24
        if self.left_count:
            self.left_percent=self.config[self.config["Axis"]=="Left"]["Percent"].unique()[0]
        if self.right_count:
            self.right_percent=self.config[self.config["Axis"]=="Right"]["Percent"].unique()[0]
        if self.group_bar_no:
            self.group_bar_width = self.bar_width / self.group_bar_no
            self.group_bar_delta =range(1,self.group_bar_no+1)
            self.x = mdates.date2num(self.data_df[self.time_col])
            self.group_bar_x=[v-self.bar_width/2+self.group_bar_width/2 for v in self.x]
        else:
            self.x = self.data_df[self.time_col]
        if self.right_count > 0:
            self.ax2 = self.ax1.twinx()
            self.ax2.tick_params(axis='y', labelcolor="r")
            self.ax1.set_zorder(1)  # default zorder is 0 for ax1 and ax2
            self.ax1.patch.set_visible(False)  # prevents ax1 from hiding ax2
            self.ax1.grid(False)
            self.ax2.grid(axis='y')
            self.ax2.set_axisbelow(True)
        return True

    def plot_line(self):
        color = 0
        df = self.data_df
        if self.overall_chart:
            x=[]
            y=[]
            for index,row in self.config.iterrows():
                x.append(row["Kpi_name"])
                y.append(np.sum(self.data_df[row["Kpi_name"]]))
            self.ax1.bar(x,y)
        else:
            for index, row in self.config.iterrows():
                plot_para = {"label": row["Legend_label"]}
                plot_para["color"] = "C" + str(color)
                if row["Axis"] == "Left":
                    ax = self.ax1
                elif row["Axis"] == "Right":
                    ax = self.ax2
                else:
                    ax = None

                try:
                    df[row["Kpi_name"]] = eval(row["Formula"])
                    if row["Kpi_name"]=="SgNB_Setup_SR_eNBR":
                        print("lalala")
                except (KeyError, SyntaxError, TypeError, ValueError, NameError) as e:
                    print("wrong formula")
                    print(row["Kpi_name"], row["Formula"])
                    print(type(e), e)
                    # traceback.print_exc()
                    df[row["Kpi_name"]] = float('nan')
                    self.ax1.set_title("{} , {}".format(row["Chart_tile"],"wrong formula"))


                y = self.data_df[row["Kpi_name"]]
                if row["Chart_type"] == "Line":
                    plot_para["marker"]="."
                    ax.plot(self.x, y, **plot_para)
                elif row["Chart_type"] == "Dotted line":
                    plot_para["ls"] = "--"
                    ax.plot(self.x, y, **plot_para)
                elif row["Chart_type"] == "Bar":
                    plot_para["align"] = "center"
                    plot_para["width"] = self.bar_width
                    ax.bar(self.x, y, **plot_para)
                elif row["Chart_type"] == "StackedBar":
                    plot_para["align"] = "center"
                    plot_para["width"] = self.bar_width
                    plot_para["bottom"] = self.bottom
                    ax.bar(self.x, y, **plot_para)
                    self.bottom += y
                elif row["Chart_type"] == "GroupBar":
                    plot_para["align"] = "center"
                    plot_para["width"] = self.group_bar_width
                    ax.bar(self.group_bar_x, y, **plot_para)
                    self.group_bar_x = [v +self.group_bar_width for v in self.group_bar_x]
                    self.bottom += y
                color += 1

    def post_plot(self):
        if self.group_bar_no:
            self.ax1.xaxis_date()
        if self.left_count:
            legend_para = copy.copy(GENERAL_LEGEND_CONFIG_LEFT)
            if self.small_legend == True:
                legend_para.update(self.small_legend_config)
            else:
                legend_para["ncol"] = math.ceil(self.left_count / 2)
            self.ax1.legend(**legend_para)
        if self.right_count:
            legend_para = copy.copy(GENERAL_LEGEND_CONFIG_RIGHT)
            legend_para["ncol"] = math.ceil(self.right_count / 2)
            self.ax2.legend(**legend_para)
        if not self.overall_chart:
            if self.time_col == "Date":
                self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
            elif self.time_col == "Time":
                self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H'))
            if self.time_col == "Date":
                self.ax1.set_xlim(min(self.data_df[self.time_col]) - datetime.timedelta(days=1),
                                  max(self.data_df[self.time_col]) + datetime.timedelta(days=1))
            elif self.time_col == "Time":
                self.ax1.set_xlim(min(self.data_df[self.time_col]) - datetime.timedelta(hours=1),
                                  max(self.data_df[self.time_col]) + datetime.timedelta(hours=1))
            self.widget.canvas.fig.autofmt_xdate()

        if self.left_percent:
            self.ax1.yaxis.set_major_formatter(mtick.PercentFormatter())
        if self.right_count and self.right_percent:
            self.ax2.yaxis.set_major_formatter(mtick.PercentFormatter())

        self.widget.canvas.fig.tight_layout()

    def plot(self, config_df, data_df, data_level,column_value, time_col, small_legend_config):
        self.data_df = data_df
        self.config_df = config_df
        self.data_level=data_level
        self.column_value = column_value
        self.time_col = time_col
        self.small_legend_config = small_legend_config
        self.grid_row=self.grid_column=0

        for chart_no in self.config_df["Chart_no"].unique():
            self.chart_no = chart_no
            flag=self.pre_plot()
            if flag:
                if self.special_chart:
                    getattr(special_plot, self.function_name)(self.data_df, self.ax1,self.left_percent)
                else:
                    self.plot_line()
                self.post_plot()


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
    sc.test_plot()

    sys.exit(app.exec_())
