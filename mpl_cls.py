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

GENERAL_LEGEND_CONFIG_LEFT = {"loc": "upper left", "bbox_to_anchor": (-0.15, 1.15), "frameon": False, "fontsize": "small"}
GENERAL_LEGEND_CONFIG_RIGHT = {"loc": "upper right", "bbox_to_anchor": (1, 1.15), "frameon": False, "fontsize": "small"}

SPECIAL_LEGEND_CONFIG={"bbox_to_anchor":(-0.17,1.15),"ncol":1,"fontsize":"x-small",
                                   }
RIGHT_COLORS="rgcmy"
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

    def plot(self, configs, df, GP, column_value, time_col,special_legend_title):
        for chart_no in range(1, len(configs) + 1):
            rect = QtWidgets.QApplication.desktop().screenGeometry()
            if GP == 3600:
                width = rect.width() - 100
            if GP == 3600 * 24:
                width = rect.width() // 2 - 50

            height = rect.height() // 2 - 50
            widget = MplWidget(parent=self.scroll_widget)
            widget.setFixedWidth(width)
            widget.setFixedHeight(height)
            ax1 = widget.canvas.fig.add_subplot(111)
            right = False
            if GP == 3600:
                self.gridlayout.addWidget(widget, chart_no - 1, 0)
            elif GP == 3600 * 24:
                self.gridlayout.addWidget(widget, (chart_no - 1) // 2, (chart_no - 1) % 2)

            self.widgets[chart_no] = widget
            left_count = 0
            right_count = 0
            bottom=0
            for config in configs[chart_no]:
                ax1.set_title("{} , {}".format(config["Chart_tile"], column_value))

                try:
                    df[config["Kpi_name"]] = eval(config["eval_exp"])
                except (KeyError, SyntaxError, TypeError) as e:
                    print("wrong formula", config)
                    print(e)
                    # traceback.print_exc()
                    df[config["Kpi_name"]] = None
                    ax1.set_title("{} , {}".format(config["Chart_tile"], "wrong formula"))
                x = df[time_col]
                y = df[config["Kpi_name"]]
                plot_para = {"label": config["Kpi_name"]}
                if config["Axis"] == "Right":
                    right_count += 1
                    if right == False:
                        ax2 = ax1.twinx()
                        right = True
                        ax2.tick_params(axis='y', labelcolor="r")

                    ax = ax2
                    plot_para["color"] = RIGHT_COLORS[right_count-1]
                    # if ax.get_ylabel() == "":
                    #     ax.set_ylabel(config["Kpi_name"], color="r")
                elif config["Axis"] == "Left":
                    left_count += 1
                    ax = ax1

                if config["Chart_type"] == "Line":
                    ax.plot(x, y, **plot_para)
                elif config["Chart_type"] == "Bar":
                    plot_para["align"] = "center"
                    plot_para["alpha"] = 0.8
                    plot_para["width"] = 0.8 if GP == 3600 * 24 else 1 / len(x)
                    ax.bar(x, y, **plot_para)
                elif config["Chart_type"]=="StackedBar":
                    plot_para["align"] = "center"
                    plot_para["alpha"] = 0.8
                    plot_para["width"] = 0.8 if GP == 3600 * 24 else 1 / len(x)
                    plot_para["bottom"]=bottom
                    ax.bar(x, y, **plot_para)
                    bottom+=y


                elif config["Chart_type"] == "Dotted line":
                    plot_para["linestyle"] = "--"
                    ax.plot(x, y, **plot_para)
                if config["Percent"] == True:
                    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
                # ax.set_xlim(min(x), max(x))

            legend_para=copy.copy(GENERAL_LEGEND_CONFIG_LEFT)
            if config["Chart_tile"] in special_legend_title:
                legend_para.update(SPECIAL_LEGEND_CONFIG)
            else:
                legend_para["ncol"]=math.ceil(left_count / 2)
            ax1.legend(**legend_para)
            if GP==3600*24:
                ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
            elif GP==3600:
                ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))

            # ax1.legend(loc='upper left', bbox_to_anchor=(-0.15,1.15), frameon=False, fontsize='small',ncol=1)
            # ax1.legend(loc='upper left', bbox_to_anchor=(-0.15,1.15),frameon=False, fontsize='x-small',ncol=1)
            if right:
                legend_para = copy.copy(GENERAL_LEGEND_CONFIG_RIGHT)
                legend_para["ncol"] = math.ceil(right_count / 2)
                ax2.legend(**legend_para)
                if GP == 3600 * 24:
                    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
                elif GP == 3600:
                    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))

            self.widgets[chart_no].canvas.fig.autofmt_xdate()
            self.widgets[chart_no].canvas.fig.tight_layout()

    def test_plot(self):
        rect = QtWidgets.QApplication.desktop().screenGeometry()
        width = rect.width() // 2 - 50
        height = rect.height() // 2 - 50

        widget = MplWidget(parent=self.scroll_widget)
        widget.setFixedWidth(width)
        widget.setFixedHeight(height)
        axes = widget.canvas.fig.add_subplot(111)

        x = np.arange(10)
        y = np.random.random(10)
        y_mean = [np.mean(y)] * len(x)

        axes.plot(x, y_mean)
        self.gridlayout.addWidget(widget, 0, 0)

        widget = MplWidget(parent=self.scroll_widget)
        widget.setFixedWidth(width)
        widget.setFixedHeight(height)
        axes = widget.canvas.fig.add_subplot(111)

        objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
        y_pos = np.arange(len(objects))
        performance = [10, 8, 6, 4, 2, 1]

        axes.bar(y_pos, performance, align='center', alpha=0.5)
        self.gridlayout.addWidget(widget, 0, 1)

        widget = MplWidget(parent=self.scroll_widget)
        widget.setFixedWidth(width)
        widget.setFixedHeight(height)
        axes = widget.canvas.fig.add_subplot(111)

        objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
        y_pos = np.arange(len(objects))
        performance = [10, 8, 6, 4, 2, 1]

        axes.bar(y_pos, performance, align='center', alpha=0.5)
        self.gridlayout.addWidget(widget, 1, 0)

        widget = MplWidget(parent=self.scroll_widget)
        widget.setFixedWidth(width)
        widget.setFixedHeight(height)
        axes = widget.canvas.fig.add_subplot(111)

        objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
        y_pos = np.arange(len(objects))
        performance = [10, 8, 6, 4, 2, 1]

        axes.bar(y_pos, performance, align='center', alpha=0.5)
        self.gridlayout.addWidget(widget, 1, 1)

        # widget = MplWidget(parent=self.scroll_widget)
        # widget.setFixedWidth(width)
        # widget.setFixedHeight(height)
        # axes = widget.canvas.fig.add_subplot(111)
        #
        # objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
        # y_pos = np.arange(len(objects))
        # performance = [1, 2, 3, 4, 5, 6]
        #
        # axes.bar(y_pos, performance, align='center', alpha=0.5)
        # self.gridlayout.addWidget(widget, 0, 0)


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

    myWin = QtWidgets.QMainWindow()
    sc = ScrollaleChartsArea(myWin)
    myWin.setCentralWidget(sc)
    myWin.show()
    sc.test_plot()

    sys.exit(app.exec_())
