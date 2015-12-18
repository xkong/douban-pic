# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'checkdlg.ui'
#
# Created: Fri Sep 02 22:08:57 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class Ui_dialog(object):

    def setupUi(self, dialog):
        dialog.setObjectName(u"dialog")
        dialog.resize(433, 394)
        dialog.setMaximumSize(QtCore.QSize(433, 394))
        dialog.setWindowTitle(QtGui.QApplication.translate("dialog", "选择要下载的页", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonBox = QtGui.QDialogButtonBox(dialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 20, 341, 91))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u"buttonBox")
        self.tableWidget = QtGui.QTableWidget(dialog)
        self.tableWidget.setGeometry(QtCore.QRect(40, 50, 161, 301))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("dialog", "页数", None, QtGui.QApplication.UnicodeUTF8))
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.btnSelectAll = QtGui.QPushButton(dialog)
        self.btnSelectAll.setGeometry(QtCore.QRect(251, 111, 77, 25))
        self.btnSelectAll.setText(QtGui.QApplication.translate("dialog", "全选", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectAll.setObjectName(_fromUtf8("btnSelectAll"))
        self.btnUnselectAll = QtGui.QPushButton(dialog)
        self.btnUnselectAll.setGeometry(QtCore.QRect(334, 111, 77, 25))
        self.btnUnselectAll.setText(QtGui.QApplication.translate("dialog", "全消", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUnselectAll.setObjectName(_fromUtf8("btnUnselectAll"))
        self.label = QtGui.QLabel(dialog)
        self.label.setGeometry(QtCore.QRect(260, 170, 141, 51))
        self.label.setText(QtGui.QApplication.translate("dialog", "选择需要下载的页，每页\n"
"有图片100张", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        item = self.tableWidget.horizontalHeaderItem(0)

