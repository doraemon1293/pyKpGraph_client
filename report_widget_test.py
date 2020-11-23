import openpyxl
import report_widget
import util
from PyQt5 import QtWidgets
import traceback
import sys
import pandas as pd
from parameters import *


class Report_widget_tester():
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

    def test(self):

        def excepthook(exc_type, exc_value, exc_tb):
            tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
            print("error catched!:")
            print("error message:\n", tb)
            QtWidgets.QApplication.quit()
            # or QtWidgets.QApplication.exit(0)

        sys.excepthook = excepthook
        app = QtWidgets.QApplication([])
        self.ppo_report_widget = report_widget.Ppo_report_widget(self.ppo_config, self.query_config,self.agg_function,
                                                                 self.additional_kpi, self.conditional_kpi,self.ignore_fields)
        self.ppo_report_widget.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    tester = Report_widget_tester()
    tester.load_config("template.xlsx")
    tester.test()
