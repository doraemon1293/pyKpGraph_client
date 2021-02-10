import matplotlib

import sys
import matplotlib.ticker as mtick
import math
from numpy import log10
import copy
import textwrap

matplotlib.use('Qt5Agg')
import numpy as np
import traceback
from PyQt5 import QtWidgets
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  # , NavigationToolbar2QT as NavigationToolbar
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

GENERAL_LEGEND_CONFIG_LEFT = {"loc": "upper left", "bbox_to_anchor": (-0.1, 1.12), "frameon": False, "fontsize": 10}
GENERAL_LEGEND_CONFIG_RIGHT = {"loc": "upper right", "bbox_to_anchor": (1.1, 1.12), "frameon": False, "fontsize": 10}
TITLE_PAD = 25
SMALLE_LEGEND_TITLE_PAD = 40
SMALLE_LEGEND_FONT_SIZE = 6


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
        self.toolbar = NavigationToolbar(self.canvas, self)
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
            self.function_name = self.config["Special_chart"].unique()[0]
        else:
            self.special_chart = False
        # if "Small_legend" in self.config.columns and self.config["Small_legend"].unique()[0] == True:
        #     self.small_legend = True
        # else:
        #     self.small_legend = False
        if self.time_col == "Time" or "Wide_chart" in self.config.columns and self.config["Wide_chart"].unique()[
            0] == True:
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
        if "Not_for_cluster_level" in self.config.columns and self.config["Not_for_cluster_level"].unique()[0] == True:
            self.not_for_cluster_level = True
        else:
            self.not_for_cluster_level = False

        if "Trx_Chart" in self.config.columns and self.config["Trx_Chart"].unique()[0] == True:
            self.trx_chart = True
        else:
            self.trx_chart = False
        if "Small Legend" in self.config.columns and self.config["Small Legend"].unique()[0] == True:
            self.small_legend = True
        else:
            self.small_legend = False
        if "ETH_port_chart" in self.config.columns and pd.notnull(self.config["ETH_port_chart"].unique()[0]):
            self.eth_port_chart = self.config["ETH_port_chart"].unique()[0]
        else:
            self.eth_port_chart = False

        self.title = self.config["Chart_title"].unique()[0]

        rect = QtWidgets.QApplication.desktop().screenGeometry()
        height = rect.height() // 2 - 50

        if width_chart:
            width = rect.width() - 100
            if self.grid_column == 1:
                self.grid_row += 1
                self.grid_column = 0
            self.gridlayout.addWidget(self.widget, self.grid_row, self.grid_column, 1, 2)
            self.grid_row += 1
            self.grid_column = 0
        else:
            width = rect.width() // 2 - 50
            self.gridlayout.addWidget(self.widget, self.grid_row, self.grid_column)
            self.grid_column += 1
            if self.grid_column == 2:
                self.grid_row += 1
                self.grid_column = 0
        self.widget.setFixedWidth(width)
        self.widget.setFixedHeight(height)
        self.ax1 = self.widget.canvas.fig.add_subplot(111)
        self.ax1.ticklabel_format(useOffset=False)
        if self.layer and self.layer != "All Site":
            self.ax1.set_title("{} , {} {}".format(self.title, self.column_value, self.layer), pad=TITLE_PAD)
        else:
            self.ax1.set_title("{} , {}".format(self.title, self.column_value, ), pad=TITLE_PAD)
        if self.not_for_cell_level and self.agg_level == "Cell":
            self.ax1.set_title("{} , {}".format(self.title, "Not for cell level"), pad=TITLE_PAD)
            return False
        if self.not_for_cluster_level and self.agg_level == "Cluster":
            self.ax1.set_title("{} , {}".format(self.title, "Not for cluster level"), pad=TITLE_PAD)
            return False
        self.ax1.grid(axis='y')
        self.ax1.set_axisbelow(True)
        self.ax1.ticklabel_format(style='plain', useOffset=False)
        self.left_count = len(self.config[self.config["Axis"] == "Left"])
        self.right_count = len(self.config[self.config["Axis"] == "Right"])
        if "Unit" in self.config.columns:
            if self.left_count:
                self.left_unit = self.config[self.config["Axis"] == "Left"]["Unit"].unique()[0]
                if pd.isnull(self.left_unit):
                    self.left_unit = ""

            if self.right_count:
                self.right_unit = self.config[self.config["Axis"] == "Right"]["Unit"].unique()[0]
                if pd.isnull(self.right_unit):
                    self.right_unit = ""

        self.bottom = 0
        self.group_bar_no = self.config[self.config["Chart_type"] == "GroupBar"].shape[0]
        self.bar_width = 0.8 if self.time_col == "Date" else 0.8 / 24

        if self.group_bar_no:
            self.group_bar_width = self.bar_width / self.group_bar_no
            self.group_bar_delta = range(1, self.group_bar_no + 1)
            self.x = mdates.date2num(self.data_df[self.time_col])
            self.group_bar_x = [v - self.bar_width / 2 + self.group_bar_width / 2 for v in self.x]
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
            self.ax2.ticklabel_format(style='plain', useOffset=False)
            self.ax1.format_coord = util.make_format(self.ax1, self.ax2, self.time_col)

        if self.left_count:
            self.ax1.set_ylabel(self.left_unit)
        if self.right_count:
            self.ax2.set_ylabel(self.right_unit)
        return True

    def plot_line(self):
        color = 0
        df = self.data_df
        if self.overall_chart:
            x = []
            y = []
            for index, row in self.config.iterrows():
                df = self.data_df
                sum_df = pd.Series()
                for kpi in row["Kpis"]:
                    sum_df[kpi] = np.sum(df[kpi])
                df = sum_df
                x.append(row["Legend_label"])
                y.append(eval(row["Formula"]))
            self.ax1.bar(x, y, tick_label=[str(label) for label in x])

        elif self.trx_chart and self.agg_level == "Cell":
            self.group_bar_no = len(self.trx_df["TRXNo"].unique())
            self.group_bar_width = self.bar_width / self.group_bar_no
            self.group_bar_delta = range(1, self.group_bar_no + 1)
            self.x = mdates.date2num(self.data_df[self.time_col])
            self.group_bar_x = [v - self.bar_width / 2 + self.group_bar_width / 2 for v in self.x]
            for index, row in self.config.iterrows():
                for trx_no in sorted(self.trx_df["TRXNo"].unique()):
                    df = self.trx_df.copy()
                    df = df[df["TRXNo"] == trx_no]
                    plot_para = {"label": "TRX - {}".format(trx_no)}
                    plot_para["color"] = "C" + str(color)
                    if row["Axis"] == "Left":
                        ax = self.ax1
                    elif row["Axis"] == "Right":
                        ax = self.ax2
                    else:
                        ax = None
                    try:
                        df[row["Kpi_name"]] = eval(row["Formula"])

                    except (KeyError, SyntaxError, TypeError, ValueError, NameError) as e:
                        print("wrong formula")
                        print(row["Kpi_name"], row["Formula"])
                        print(type(e), e)
                        # traceback.print_exc()
                        df[row["Kpi_name"]] = float('nan')
                        # self.ax1.set_title("{} , {}".format(row["Chart_tile"],"wrong formula"))
                    y = df[row["Kpi_name"]]
                    if row["Chart_type"] == "Line":
                        plot_para["marker"] = "."
                        ax.plot(self.x, y, **plot_para)
                    elif row["Chart_type"] == "Bar":
                        plot_para["align"] = "center"
                        plot_para["width"] = self.group_bar_width
                        ax.bar(self.group_bar_x, y, **plot_para)
                        self.group_bar_x = [v + self.group_bar_width for v in self.group_bar_x]
                    color += 1
        else:
            if self.eth_port_chart:
                df = self.eth_df.copy()
                df = df[df["Port No"] == self.eth_port_chart]
            else:
                df = self.data_df

            for index, row in self.config.iterrows():
                if self.trx_chart:
                    plot_para = {"label": "TRX"}
                elif self.small_legend:
                    plot_para = {"label": textwrap.fill(row["Legend_label"], 16)}
                else:
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

                except (KeyError, SyntaxError, TypeError, ValueError, NameError) as e:
                    print("wrong formula")
                    print(row["Kpi_name"], row["Formula"])
                    print(type(e), e)
                    # traceback.print_exc()
                    df[row["Kpi_name"]] = float('nan')
                    # self.ax1.set_title("{} , {}".format(row["Chart_tile"],"wrong formula"))

                y = df[row["Kpi_name"]]
                if not df.empty:
                    if row["Chart_type"] == "Line":
                        plot_para["marker"] = "."
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
                        self.group_bar_x = [v + self.group_bar_width for v in self.group_bar_x]
                        # self.bottom += y
                    color += 1

    def post_plot(self):
        if self.group_bar_no:
            self.ax1.xaxis_date()
        if self.left_count:
            legend_para = copy.copy(GENERAL_LEGEND_CONFIG_LEFT)
            if self.small_legend:
                # self.ax1.set_title(self.ax1.get_title(),pad=SMALLE_LEGEND_TITLE_PAD)
                self.ax1.set_title(self.ax1.get_title(), pad=0)
                legend_para["bbox_to_anchor"] = [-0.2, 1.1]
                legend_para["fontsize"] = SMALLE_LEGEND_FONT_SIZE
                legend_para["ncol"] = 1
            elif self.left_count >= 4:
                legend_para["fontsize"] = SMALLE_LEGEND_FONT_SIZE
                legend_para["ncol"] = math.ceil(self.left_count / 2)
                legend_para["columnspacing"] = 0.2

            else:
                legend_para["ncol"] = len(self.ax1.get_legend_handles_labels()[0])
            self.ax1.legend(**legend_para)

        if self.right_count:
            legend_para = copy.copy(GENERAL_LEGEND_CONFIG_RIGHT)
            if self.right_count >= 4:
                legend_para["fontsize"] = SMALLE_LEGEND_FONT_SIZE
                legend_para["ncol"] = math.ceil(self.left_count / 2)
            else:
                legend_para["ncol"] = len(self.ax2.get_legend_handles_labels()[0])
            self.ax2.legend(**legend_para)
        if not self.overall_chart:
            if self.time_col == "Date":
                self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
            elif self.time_col == "Time":
                self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H'))
            if self.time_col == "Date":
                self.ax1.set_xlim(min(self.data_df[self.time_col]) - datetime.timedelta(days=0.5),
                                  max(self.data_df[self.time_col]) + datetime.timedelta(days=0.5))
            elif self.time_col == "Time":
                self.ax1.set_xlim(min(self.data_df[self.time_col]) - datetime.timedelta(hours=0.5),
                                  max(self.data_df[self.time_col]) + datetime.timedelta(hours=0.5))
            self.widget.canvas.fig.autofmt_xdate()
            for i, change_day_line in enumerate(self.change_day_lines):
                self.ax1.axvline(x=change_day_line, color="k")

        if self.overall_chart or self.small_legend:
            self.widget.canvas.fig.tight_layout(pad=0.7)

    def plot(self, config_df, data_df, agg_level, column_value, time_col, trx_df, eth_df, layer, change_day_lines):
        self.data_df = data_df
        self.config_df = config_df
        self.agg_level = agg_level
        self.column_value = column_value
        self.time_col = time_col
        # self.small_legend_config = small_legend_config
        self.grid_row = self.grid_column = 0
        self.trx_df = trx_df
        self.eth_df = eth_df
        self.layer = layer
        self.change_day_lines = change_day_lines
        for chart_no in self.config_df["Chart_no"].unique():
            self.chart_no = chart_no
            flag = self.pre_plot()
            if flag:
                if self.special_chart:
                    getattr(special_plot, self.function_name)(self.data_df, self.ax1, self.left_unit)
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
