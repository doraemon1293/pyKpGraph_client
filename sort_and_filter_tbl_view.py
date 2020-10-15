import sys
import traceback
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt,QSortFilterProxyModel
import PyQt5.QtCore as QtCore



class PandaDataFrameModel(QAbstractTableModel):

    def __init__(self, df):
        QAbstractTableModel.__init__(self)
        self.df = df.copy()
        sortermodel = QSortFilterProxyModel()
        sortermodel.setSourceModel(self)

    def rowCount(self, parent=None):
        return self.df.shape[0]

    def columnCount(self, parnet=None):
        return self.df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self.df.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.df.columns[col]
        return None

class Sort_and_filter_tbl_view(QtWidgets.QWidget):
    def __init__(self, parent=None,df=pd.DataFrame()):
        #init
        super(Sort_and_filter_tbl_view, self).__init__(parent)
        #layout
        self.df=df
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.tbl_view = QtWidgets.QTableView(self)
        self.comboBox = QtWidgets.QComboBox(self)
        self.label = QtWidgets.QLabel(self)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.tbl_view, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.setLayout(self.gridLayout)

        #comboBox and label
        self.comboBox.addItems([x for x in self.df.columns])
        self.label.setText("Wildcard Search")

        #model
        self.model = PandaDataFrameModel(self.df)
        self.tbl_view.setSortingEnabled(True)

        #proxymodel
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(False)
        self.tbl_view.setModel(self.proxy_model)

        #connect
        self.lineEdit.textChanged.connect(self.on_lineEdit_textChanged)
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)

    @QtCore.pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        # search = QtCore.QRegExp(text,
        #                         QtCore.Qt.CaseInsensitive,
        #                         QtCore.QRegExp.RegExp
        #                         )

        self.proxy_model.setFilterWildcard(text)

    @QtCore.pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        self.proxy_model.setFilterKeyColumn(index)

if __name__ == '__main__':
    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("error catched!:")
        print("error message:\n", tb)
        QtWidgets.QApplication.quit()
        # or QtWidgets.QApplication.exit(0)


    sys.excepthook = excepthook

    df = pd.DataFrame({'a': ['AAA', 'CCC', 'BBB','DDD'],
                       'b': [400, 200, 100,300],
                       'c': ['a', 'b', 'c','d']})
    app = QApplication(sys.argv)
    # model = PandaDataFrameModel(df)
    # view = QTableView()
    # view.setSortingEnabled(True)
    #
    # view.setModel(model)
    # view.resize(800, 600)
    # view.show()

    obj=Sort_and_filter_tbl_view(df=df)
    obj.show()
    sys.exit(app.exec_())