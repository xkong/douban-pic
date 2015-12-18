# coding:utf-8

import sys
import threading
import time
import thread
import urllib

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from dbpic_ui import Ui_MainWindow
from check_image_dialog import Check
from backend import Douban, logging

# globals
lst = []
d = 0
recursion = 0
failed = []
kv = {}


class DoubanPic(QMainWindow):

    def __init__(self, parent=None):
        super(DoubanPic, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.progressBar.setValue(0)

        self.photourls = []
        self.checkedPages = []
        self.finalLinks = []

        self.connect(self.ui.pushButton, SIGNAL("clicked()"), self.getPic)
        self.connect(self.ui.lineEdit, SIGNAL("returnPressed()"), self.getPic)

    def getPic(self):
        global lst
        lst = []
        self.photourls = []
        self.db = Douban(self)
        self.ui.progressBar.setValue(0)
        self.orgLink = unicode(self.ui.lineEdit.text())
        self.dLink = self.db.tidyLink(self.orgLink.strip())
        if not self.dLink:
            self.ui.lineEdit.setText("")
            self.ui.lineEdit.setFocus()
            return
        logging.info("Ready to analysis album info")
        self.photourls = self.db.getPhotoLinks(self.dLink)
        if self.db.photoCount >= 100:
            self.check()
            for i in self.checkedPages:
                self.finalLinks.extend(self.photourls[i * 100: (i + 1) * 100 - 1])
        else:
            self.finalLinks = self.photourls
        if not self.finalLinks:
            self.ui.statusbar.showMessage(u"没有选择要下载的图片...")
            self.ui.lineEdit.setFocus()
            return
        self.ui.progressBar.setRange(0, len(self.finalLinks))
        lst = self.finalLinks
        for filename in lst:
            fname = filename.split("/")[-1]
            fname = "photos/%s" % (fname)
            kv[fname] = 0
        tasks = []
        self.ui.statusbar.showMessage(u"开始下载图片...")
        logging.info("Ready to get pics")
        if QThread.idealThreadCount() >= 10:
            threadCount = QThread.idealThreadCount()
        else:
            threadCount = 10
        for i in range(threadCount):
            m = MutiDl(self)
            tasks.append(m)
        for task in tasks:
            time.sleep(0.5)
            task.start()
        logging.info("Muti DL started.")
        while self.isAlive(tasks):
            time.sleep(0.5)
            self.ui.progressBar.setValue(d)
        self.ui.progressBar.setValue(len(self.finalLinks))
        f = open("FailedFiles.txt", "a")
        for filename in failed:
            f.write("%s," % filename)
        f.write("\n")
        f.close()
        self.db.alert(u"所有图片下载完成！")
        logging.info("Done!")
        self.ui.statusbar.showMessage(u"")
        del self.db
        del m
        self.ui.lineEdit.setFocus()
        self.ui.lineEdit.selectAll()

    def check(self):
        if not self.photourls:
            QMessageBox.warning(self, u"提示", u"您还没有获取下载地址……")
            return
        d = Check(len(self.photourls), self)
        if d.exec_():
            self.checkedPages = d.checkedPages

    def isAlive(self, tasks):
        for task in tasks:
            if task.isAlive():
                return True
        return False


class MutiDl(threading.Thread):

    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent
        self.photoDir = "photos"
        self.lock = threading.RLock()

    def __del__(self):
        global d
        d = 0

    def dl(self, url, filename):
        global d
        global recursion
        global kv
        if kv[filename] != 0:
            logging.info("This is the %s time of DL image %s" % (kv[filename], filename))
        try:
            urllib.urlretrieve(url, filename)
        except IOError, e:
            if hasattr(e, "reason"):
                logging.error(":[%s]While getting %s,URLError:%s" % (self.getName(), filename, e.reason))
            elif hasattr(e, "code"):
                logging.error(":[%s]While getting %s,HttpError:%s" % (self.getName(), filename, e.code))
            else:
                logging.error(":[%s]While getting %s,Error:%s" % (self.getName(), filename, e))
            time.sleep(1)
            thread.start_new_thread(self.dl, (url, filename))
            if kv[filename] >= 4:
                global failed
                self.lock.acquire()
                if filename not in failed:
                    failed.append(filename)
                self.lock.release()
                logging.error("%s failed." % filename)
                return
            kv[filename] += 1
        else:
            if kv[filename] != 0:
                logging.info("IMAGE %s DL ok!" % filename)
            d += 1

    def run(self):
        while True:
            global lst
            try:
                self.lock.acquire()
                url = lst.pop()
                self.lock.release()
                filename = url.split("/")[-1]
            except IndexError:
                break
            else:
                self.dl(url, "%s/%s" % (self.photoDir, filename))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = DoubanPic()
    db.show()
    sys.exit(app.exec_())
