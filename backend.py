#coding:utf-8

import sys
import os
import re
import urllib
import threading
from Queue import Queue
import logging

from PyQt4.QtCore import *
from PyQt4.QtGui import *


def initlog():
    #Logging.
    logger=logging.getLogger()
    logfile="dbpic.log"
    hdlr=logging.FileHandler("dbpic.log")
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return logger
logging=initlog()
logging.info("Start..")


photourls=[]
d=0
lst=[]
class Douban(threading.Thread):
    def __init__(self,parent=None):
        threading.Thread.__init__(self)
        self.parent=parent
        self.photoCount=0
        self.photoLinks=[]
        self.photoDir="photos"
        if not os.path.exists(self.photoDir):
            os.mkdir(self.photoDir)

    def __del__(self):
        self.exiting=True

    def run(self,func,*argv):
        return apply(func,argv)

    def alert(self,msg):
        QMessageBox.warning(self.parent,u"提示",msg)

    def tidyLink(self,link):
        link=link.split("?")[0]
        if not (link.startswith("http://") or link.startswith("www")):
            self.alert(u"不是一个有效的HTTP地址")
            return ""
        if  link[:3]=="www" or link[:4]=="site":
            link="http://%s"%link
        if link.split(".com")[0].split(".")[-1].find("douban")==-1:
            self.alert(u"看起来不是豆瓣的地址……")
            return ""
        if link.find("photo/")!=-1:
            if link.find(".jpg")!=-1:
                self.alert("请不要输入图片的真实地址！")
                return ""
            else:
                link=self.run(self.getAlbumLink,link)
        return link

    def getAlbumLink(self,link):
        r=self.safeOpen("GetAlbumLink",link)
        html=r.read()
        pattern=r'href="(.*?)">\xe8\xbf\x94\xe5\x9b\x9e\xe7\x9b\xb8\xe5\x86\x8c</a>'
        #p="&gt; <.*?>"
        linkText=re.findall(pattern,html)
        if linkText:
            return linkText[0]
        else:
            self.alert(u"不是一个有效的图片地址……")
            return ""

    def getPhotoLinks(self,albumLink):
        #获取图片的地址，加入列表或队列，下载用
        pageLinks=self.getPhotoPageLinks(albumLink)
        self.parent.ui.statusbar.showMessage(u"开始获取图片地址...")
        for link in pageLinks:
            self.getPhotoUrl(link)
        return self.photoLinks

    def getPhotoUrl(self,pagelink):
        #根据每一页的相册地址获取图片地址
        r=self.safeOpen("GetPhotoUrl",pagelink)
        html=r.read()
        p='<img src="(http://img\d\.douban\.com/view/photo/thumb/public/p\d+.jpg)"'
        s=re.findall(p,html)
        for url in s:
            url=url.replace("thumb","photo")
            if url not in self.photoLinks:
               self.photoLinks.append(url)

    def getPhotoPageLinks(self,albumLink):
        #获取图片分页地址
        self.parent.ui.statusbar.showMessage(u"开始获取分页地址信息...")
        logging.info("Start to get the split-page Links.")
        links=[]
        if albumLink.find("widget")!=-1 :
            pageContent=30
        else:
            if albumLink.find("online")!=-1:
                pageContent=30
            else:
                pageContent=18
        photoCount=self.run(self.getPhotoPageCount,albumLink)
        for i in range(photoCount/pageContent+1):
            purl="%s?start=%s"%(albumLink,i*pageContent)
            links.append(purl)
        return links

    def getPhotoPageCount(self,albumLink):
        #获取相册的图片数量
        self.parent.ui.statusbar.showMessage(u"开始获取相册图片数量...")
        logging.info("Start to get the counts of album.")
        r=self.safeOpen("GetPhotoPageCount",albumLink)
        html=r.read()
        if html.find("album-info")!=-1:
        #pattern=r'<span class="pl">(\d+)&nbsp;\xe5\xbc\xa0'
            pattern=r'(\d+)\xe5\xbc\xa0'
        else:
            pattern=r'<span class="pl">(\d+)&nbsp;\xe5\xbc\xa0'

        c=re.findall(pattern,html)
        if c:
            photoCount=int(c[0])
            self.photoCount=photoCount
            return photoCount
        else:
            pattern=r'<span class="count">\(\xe5\x85\xb1(\d+)\xe5\xbc\xa0\)</span>'
            c=re.findall(pattern,html)
            if c:
                photoCount=int(c[0])
                self.photoCount=photoCount
                return photoCount
        self.alert(u"未能正确获取图片数量")
        logging.error(":Failed to get the photopage account.The link is [%s]"%albumlink)
        sys.exit()
    def safeOpen(self,funcname,link):
        try:
            r=urllib.urlopen(link)
        except IOError,e:
            if hasattr(e,"reason"):
                logging.error(":While %s ,Error:%s"%(funcname,e.reason))
            elif hasattr(e,"code"):
                logging.error(":While %s ,ErrorCode:%s"%(funcname,e.code))
            else:
                logging.error(":While %s ,Error:%s"%(funcname,e))
            self.alert(u"连接到服务器错误，请查看日志。")
            sys.exit(logging.info("Sys Exit."))
        else:
            return r


if __name__=="__main__":
    pass


