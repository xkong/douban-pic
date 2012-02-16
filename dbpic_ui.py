# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dbpic.ui'
#
# Created: Wed Aug 31 23:45:03 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from icon import xpm

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(560, 346)
        MainWindow.setMaximumSize(QtCore.QSize(560, 346))
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "豆瓣相册批量下载工具 By 小彧 beta 0.4.1 build 20120214", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(xpm), QtGui.QIcon.Normal, QtGui.QIcon.On)
      #  icon.addPixmap(QtGui.QPixmap(_fromUtf8(xpm)), QtGui.QIcon.Normal, QtGui.QIcon.On)
       # icon.addPixmap(QtGui.QPixmap(_fromUtf8(xpm)), QtGui.QIcon.Active, QtGui.QIcon.Off)
       # icon.addPixmap(QtGui.QPixmap(_fromUtf8(xpm)), QtGui.QIcon.Active, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.lineEdit = MyEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 90, 371, 21))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 50, 361, 16))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "输入相册页面的地址或者相册中任一图片的页面地址：", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(420, 90, 91, 23))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "下载", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 210, 401, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 180, 61, 16))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "下载进度：", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass
class MyEdit(QtGui.QLineEdit):
    def __init__(self,parent=None):
        super(MyEdit,self).__init__(parent)
    def mousePressEvent(self,event):
        self.selectAll()
