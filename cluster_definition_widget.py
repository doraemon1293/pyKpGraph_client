from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import sys
import pandas as pd
from sort_and_filter_tbl_view import Sort_and_filter_tbl_view
import traceback
import os


class Cluster_definition_widget(QWidget):
    def __init__(self, df,mongo_client,EP_DB_NAME,CLUTSER_COL_NAME,mainwindow,parent=None):
        super(Cluster_definition_widget, self).__init__(parent)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.load_cluster_from_server_btn = QPushButton(self)
        self.load_cluster_from_server_btn.setObjectName(u"load_cluster_from_server_btn")
        self.import_custom_cluster_btn = QPushButton(self)
        self.import_custom_cluster_btn.setObjectName(u"import_custom_cluster_btn")
        self.cluster_tbl_view = Sort_and_filter_tbl_view(parent=self, df=df)
        self.cluster_tbl_view.setObjectName(u"cluster_tbl_view")

        self.verticalLayout.addWidget(self.load_cluster_from_server_btn)
        self.verticalLayout.addWidget(self.import_custom_cluster_btn)
        self.verticalLayout.addWidget(self.cluster_tbl_view)

        self.setWindowTitle("cluster_definition_widget")
        self.load_cluster_from_server_btn.setText("Load Cluster Definition from Server")
        self.import_custom_cluster_btn.setText("Import Custom Cluster Definition")

        self.setLayout(self.verticalLayout)

        self.cluster_col=mongo_client[EP_DB_NAME][CLUTSER_COL_NAME]
        self.mainwindow=mainwindow

        self.import_custom_cluster_btn.clicked.connect(self.on_import_custom_cluster_btn_clicked)
        self.load_cluster_from_server_btn.clicked.connect(self.on_load_cluster_from_server_btn_clicked)

    def on_import_custom_cluster_btn_clicked(self):
        fn=QFileDialog.getOpenFileName(self, "Open cluster definition file", os.getcwd(), "*.xlsx")[0]
        if fn!="":
            df=pd.read_excel(fn)
            df.sort_index(axis=1,inplace=True)
            if list(df.columns)==["Cluster","Site"]:
                df=df.astype({"Cluster":str,"Site":str})
                self.cluster_tbl_view.model.df=df
                self.mainwindow.cluster_def=df
                self.mainwindow.cluster_combo_box.clear()
                self.mainwindow.cluster_combo_box.addItems(sorted(df["Cluster"].unique()))
                self.cluster_tbl_view.model.layoutChanged.emit()

            else:
                QtWidgets.QErrorMessage(self).showMessage("Wrong format, title must be Site Cluster")

    def on_load_cluster_from_server_btn_clicked(self):
        df=pd.DataFrame(list(self.cluster_col.find({},{"_id":0})))
        df.sort_index(axis=1, inplace=True)
        df = df.astype({"Cluster": str, "Site":str})
        self.cluster_tbl_view.model.df=df
        self.mainwindow.cluster_def = df
        self.mainwindow.cluster_definition_widget.show()
        self.mainwindow.cluster_combo_box.clear()
        self.mainwindow.cluster_combo_box.addItems(sorted(df["Cluster"].unique()))
        self.cluster_tbl_view.model.layoutChanged.emit()


if __name__ == "__main__":
    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("error catched!:")
        print("error message:\n", tb)
        QtWidgets.QApplication.quit()
        # or QtWidgets.QApplication.exit(0)


    sys.excepthook = excepthook
    df = pd.DataFrame({'a': ['AAA', 'CCC', 'BBB', 'DDD'],
                       'b': [400, 200, 100, 300],
                       'c': ['a', 'b', 'c', 'd']})
    app = QApplication([])
    myWin = Cluster_definition_widget(df=df)
    myWin.show()
    sys.exit(app.exec_())
