import matplotlib
import sys
import matplotlib.ticker as mtick

matplotlib.use('Qt5Agg')
import numpy as np
from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


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
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)


class ScrollaleChartsArea(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super(ScrollaleChartsArea, self).__init__(parent=parent)
        self.setWidgetResizable(True)
        self.recreate()

    def recreate(self):
        self.scroll_widget = QtWidgets.QWidget(self)
        self.gridlayout = QtWidgets.QGridLayout(self.scroll_widget)
        self.gridlayout.setSpacing(0)
        self.scroll_widget.setLayout(self.gridlayout)
        self.setWidget(self.scroll_widget)
        self.axes = {}
        self.widgets = {}

    def plot(self, configs, df):
        for chart_no in range(1,len(configs)+1):
            rect = QtWidgets.QApplication.desktop().screenGeometry()
            width = rect.width() // 2 - 50
            height = rect.height() // 2 - 50
            widget = MplWidget(parent=self.scroll_widget)
            widget.setFixedWidth(width)
            widget.setFixedHeight(height)
            ax1 = widget.canvas.fig.add_subplot(111)
            right = False
            self.gridlayout.addWidget(widget, (chart_no - 1) // 2, (chart_no - 1) % 2)
            self.widgets[chart_no] = widget

            for config in configs[chart_no]:
                print(config)
                ax1.set_title(config["Chart_tile"])
                df[config["Kpi_name"]] = eval(config["eval_exp"])
                x = df["Time"]
                y = df[config["Kpi_name"]]
                plot_para = {"label": config["Kpi_name"]}
                if config["Axis"] == "Right":
                    if right == False:
                        ax2 = ax1.twinx()
                        right = True
                        ax2.tick_params(axis='y', labelcolor="r")

                    ax = ax2
                    plot_para["color"] = "r"
                    # if ax.get_ylabel() == "":
                    #     ax.set_ylabel(config["Kpi_name"], color="r")
                else:
                    ax = ax1


                if config["Chart_type"] == "Line":
                    ax.plot(x, y, **plot_para)
                elif config["Chart_type"] == "Bar":
                    plot_para["align"] = "center"
                    plot_para["alpha"] = 0.5
                    plot_para["width"] = 0.8 / len(x)
                    ax.bar(x, y, **plot_para)

                elif config["Chart_type"] == "Dotted line":
                    plot_para["linestyle"] = "--"
                    ax.plot(x, y, **plot_para)
                if config["Percent"] == True:
                    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

            ax1.legend(loc='upper left', bbox_to_anchor=(0, 1.15), framealpha=0.5, fontsize='small')
            if right:
                ax2.legend(loc='upper right', bbox_to_anchor=(1, 1.15), framealpha=0.5, fontsize='small')
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
