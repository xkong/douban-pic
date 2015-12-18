# coding:utf-8

import sys

from PySide import QtGui, QtCore

from checkdlg_ui import Ui_dialog

BASE_ROW_COUNT = 100
COLUMN_WIDTH = 150


class CheckDialog(QtGui.QDialog):

    def __init__(self, page_count, parent=None):
        super(CheckDialog, self).__init__(parent)

        self.ui = Ui_dialog()
        self.ui.setupUi(self)

        self.checked_pages = []

        self.page_count = page_count
        self.ui.tableWidget.setRowCount(self.page_count / BASE_ROW_COUNT + 1)
        self.ui.tableWidget.setColumnWidth(0, COLUMN_WIDTH)

        for i in range(self.page_count / BASE_ROW_COUNT + 1):
            if i != self.page_count / BASE_ROW_COUNT:
                end = (i + 1) * BASE_ROW_COUNT - 1
            else:
                end = self.page_count
            item = QtGui.QTableWidgetItem(u"第%s页(%s-%s)" % (i + 1, i * BASE_ROW_COUNT, end))
            item.setData(QtCore.Qt.CheckStateRole, unicode(i))
            item.setCheckState(QtCore.Qt.Checked)
            self.ui.tableWidget.setItem(i, 0, item)

        self.connect(self.ui.buttonBox, QtGui.SIGNAL("accepted()"),
                     self.accept_)
        self.connect(self.ui.btnSelectAll, QtGui.SIGNAL("clicked()"),
                     self.selectAll)
        self.connect(self.ui.btnUnselectAll, QtGui.SIGNAL("clicked()"),
                     self.unselectAll)

    def accept_(self):

        for i in range(self.ui.tableWidget.rowCount()):
            item = self.ui.tableWidget.item(i, 0)
            if item.checkState():
                self.checked_pages.append(i)
        if not self.checked_pages:
            btn = QtGui.QMessageBox.question(
                self, u"提示", u"真的什么也不选吗？",
                QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            if btn == QtGui.QMessageBox.Ok:
                self.done(0)
            else:
                self.exec_()

    def setState(self, state):
        for i in range(self.ui.tableWidget.rowCount()):
            item = self.ui.tableWidget.item(i, 0)
            item.setCheckState(state)

    def selectAll(self):
        self.setState(QtGui.Qt.Checked)

    def unselectAll(self):
        self.setState(QtCore.Qt.Unchecked)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dlg = CheckDialog(1000)
    dlg.show()
    sys.exit(app.exec_())
