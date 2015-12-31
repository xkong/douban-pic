# coding: utf-8
import sys

from PySide import QtGui

from main_ui import Ui_MainWindow
from douban_backend import BaseDoubanBackend, logging_entry


class DoubanBackend(BaseDoubanBackend):

    def alert(self, message):
        QtGui.QMessageBox.warning(self.parent, u"提示", message)

    def parent_msg(self, message):
        self.parent.msg(message)


class DoubanPic(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(DoubanPic, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.douban = DoubanBackend(self)

        self.ui.btn_download.clicked.connect(self.get_pic)
        self.ui.ipt_address.returnPressed.connect(self.get_pic)

    def get_pic(self):
        origin_url = unicode(self.ui.ipt_address.text())
        url = self.douban.check_url(origin_url)
        if not url:
            logging_entry.info("Not a valid origin_link")
            self.init()
            return
        logging_entry.info("Ready to analysis album info.")
        album_link = self.douban.get_album_link(url)
        if not album_link:
            logging_entry.info("Not a valid album_link")
            self.init()
            return
        self.msg(u"开始获取图片地址")
        photo_links = self.douban.get_photo_links(album_link)
        with open("a.txt", "w") as f:
            for i in photo_links:
                f.write(i)
                f.write("\n")

    def init(self):
        self.ui.ipt_address.setText("")
        self.ui.ipt_address.setFocus()

    def msg(self, message):
        self.ui.status_bar.showMessage(message)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    db = DoubanPic()
    db.show()
    sys.exit(app.exec_())
