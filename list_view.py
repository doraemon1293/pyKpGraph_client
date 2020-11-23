from PyQt5.QtWidgets import QDialog, QListWidget, QLineEdit, QMessageBox, QVBoxLayout, QInputDialog, QPushButton, \
    QHBoxLayout, QApplication, QDateTimeEdit, QDialogButtonBox, QDateEdit, QListView
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QDateTime, Qt
import sys
import traceback
import datetime


class MyListModel(QtCore.QAbstractListModel):
    def __init__(self, type_, arr=[], ):
        super(MyListModel, self).__init__()
        self.arr = arr
        self.type_ = type_

    def data(self, index, role):
        if role == Qt.DisplayRole:
            item = self.arr[index.row()]
            if self.type_ == "Date":
                return item.strftime("%d.%m.%Y")
            elif self.type_ == "Datetime":
                return item.strftime("%d.%m.%Y %H")
        #
        # if role == Qt.DecorationRole:
        #     status, _ = self.todos[index.row()]
        #     if status:
        #         return tick

    def rowCount(self, index):
        return len(self.arr)


class DateDialog(QDialog):
    def __init__(self, type_, parent=None):
        super(DateDialog, self).__init__(parent)

        layout = QVBoxLayout(self)

        # nice widget for editing the date
        if type_ == "Date":
            self.datetime = QDateEdit(self)
        else:
            self.datetime = QDateTimeEdit(self)

        self.datetime.setCalendarPopup(True)
        self.datetime.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.datetime)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getDateTime(type_, parent=None):
        dialog = DateDialog(type_, parent)
        result = dialog.exec_()
        date = dialog.datetime.dateTime()
        if type_ == "Date":
            return date.date().toPyDate(), result
        elif type_ == "Datetime":
            return date.toPyDateTime(), result


class ListDialog(QDialog):
    def __init__(self, type_="Date", arr=[], title="title"):
        super(ListDialog, self).__init__()
        self.title = title
        self.list_view = QListView(self)
        self.model = MyListModel(type_=type_, arr=arr)
        self.list_view.setModel(self.model)
        self.type_ = type_
        vbox = QVBoxLayout()
        for text, slot in (("Add", self.add),
                           ("Edit", self.edit),
                           ("Remove", self.remove),
                           ("Cancel", self.reject),
                           ("OK", self.accept)
                           ):
            button = QPushButton(text, parent=self)
            vbox.addWidget(button)
            button.clicked.connect(slot)
        hbox = QHBoxLayout()
        hbox.addWidget(self.list_view)
        hbox.addLayout(vbox)
        self.setLayout(hbox)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon("icon.png"))

    def add(self):
        if self.type_ == "str":
            pass
            # v, ok = QInputDialog.getText(self, title, title)
        elif self.type_ == "Date" or self.type_ == "Datetime":
            v, ok = DateDialog.getDateTime(type_=self.type_)
        if ok and v is not None:
            self.model.arr.append(v)
            self.model.layoutChanged.emit()

    def edit(self):
        indexes = self.list_view.selectedIndexes()
        if indexes:
            ind = indexes[0]
            if self.type_ == "str":
                pass
                # v, ok = QInputDialog.getText(self, title, title)
            elif self.type_ == "Date" or self.type_ == "Datetime":
                v, ok = DateDialog.getDateTime(type_=self.type_)
            if ok and v is not None:
                self.model.arr[ind.row()] = v
                self.model.layoutChanged.emit()

    def remove(self):
        indexes = self.list_view.selectedIndexes()
        if indexes:
            ind = indexes[0]
            del self.model.arr[ind.row()]
            self.list_view.clearSelection()
            self.model.layoutChanged.emit()


if __name__ == "__main__":
    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("error catched!:")
        print("error message:\n", tb)
        QtWidgets.QApplication.quit()
        # or QtWidgets.QApplication.exit(0)


    sys.excepthook = excepthook

    dates = [datetime.datetime(2020, 10, 16), datetime.datetime(2020, 10, 17), datetime.datetime(2020, 10, 18)]
    app = QApplication(sys.argv)
    dialog = ListDialog(type_="Datetime", arr=dates)
    dialog.exec_()
    # print(dialog.result())
    # if dialog.result():
    #     print(dialog.list)
    # print("--",QDialog.Accepted,QDialog.Rejected)

    print(dialog.result())
    print(dialog.model.arr)
    app.exec_()
