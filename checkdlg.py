#coding:utf-8

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from checkdlg_ui import Ui_dialog

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Check(QDialog):
    def __init__(self,pagecount,parent=None):
        super(Check,self).__init__(parent)

        self.ui=Ui_dialog()
        self.ui.setupUi(self)

        self.checkedPages=[]

        self.pageCount=pagecount
        self.ui.tableWidget.setRowCount(self.pageCount/100+1)
        self.ui.tableWidget.setColumnWidth(0,150)

        for i in range(self.pageCount/100+1):
            if i==self.pageCount/100:
                end=self.pageCount
            else:
                end=(i+1)*100-1
            item=QTableWidgetItem(_fromUtf8("第%s页(%s-%s)"%(i+1,i*100,end)))
            item.setData(Qt.CheckStateRole,unicode(i))
            item.setCheckState(Qt.Checked)
            self.ui.tableWidget.setItem(i,0,item)

        self.connect(self.ui.buttonBox,SIGNAL("accepted()"),self.test)
        self.connect(self.ui.btnSelectAll,SIGNAL("clicked()"),self.selectAll)
        self.connect(self.ui.btnUnselectAll,SIGNAL("clicked()"),self.unselectAll)

    def test(self):
        for i in range(self.ui.tableWidget.rowCount()):
            item=self.ui.tableWidget.item(i,0)
            if item.checkState()!=0:
                self.checkedPages.append(i)
        if not self.checkedPages:
            btn=QMessageBox.question(self,u"提示",u"真的什么也不选吗？",
                    QMessageBox.Ok|QMessageBox.Cancel)
            if btn==QMessageBox.Ok:
                self.done(0)
            else:
                self.exec_()
    def setState(self,state):
        for i in range(self.ui.tableWidget.rowCount()):
            item=self.ui.tableWidget.item(i,0)
            item.setCheckState(state)
    def selectAll(self):
        self.setState(Qt.Checked)
    def unselectAll(self):
        self.setState(Qt.Unchecked)
if __name__=="__main__":
    app=QApplication(sys.argv)
    dlg=Check(1000)
    dlg.show()
    sys.exit(app.exec_())
