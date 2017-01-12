# coding: utf-8
#
# xiaokong1937@gmail.com
#
# 2015/12/31
#
import logging
import re
import threading
import time
import urlparse

import requests


LOG_FILE = 'dbpic.log'
PATTERN_BACK_TO_ALBUM = ur'href="(.*?)">返回相册'
PATTERN_PHOTO_COUNT = ur"共(\d+)张"
PATTERN_PHOTO_URL = ur'<img src="(https://img\d\.douban[a-z]*\.com/view/photo/thumb/public/p\d+.jpg)"'
PATTERN_ONLINE = r'https://www.douban.com/online/(\d+)/'
PATTERN_ONLINE_ALBUM = ur'href="(https://www.douban.com/online/\d+/album/\d+/)" id="pho-num">全部\d+张'

ERROR_NOT_A_VALID_ALBUM = u"不是一个有效的豆瓣相册地址"
ERROR_NOT_A_VALID_PIC = u"不是一个有效的图片地址"
ERROR_NOT_GET_PHOTO_COUNT = u"不能获取图片数量"

MSG_GET_PIC = u"获取图片地址"
MSG_GET_PIC_OK = u"获取图片地址...完成"
MSG_GET_PIC_COUNT = u"获取图片地址完成，共获取到{}张图片"


def initlog():
    logger = logging.getLogger()
    hdlr = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return logger


logging_entry = initlog()
logging_entry.info("Start..")


def fake_headers():
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://www.douban.com/',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.douban.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/30.0.1599.'
                      '101 Safari/537.36',
    }


class BaseDoubanBackend(threading.Thread):

    def __init__(self, parent=None):
        threading.Thread.__init__(self)

        self.parent = parent

        self.photo_count = 0
        self.album_id = 0
        self.photo_links = []

        self.headers = fake_headers()
        self.link_type = 'album'  # album, online

    def __del__(self):
        self.exiting = True

    def run(self, func, *argv):
        return apply(func, argv)

    def check_url(self, origin_url):
        url = urlparse.urlparse(origin_url)

        if "douban" not in url.netloc:
            self.alert(ERROR_NOT_A_VALID_ALBUM)
            return ""

        return urlparse.urlunparse((url.scheme, url.netloc, url.path, "", "", ""))

    def get_album_link(self, link):
        # link is a link of an album
        logging_entry.info(link)
        if link.find('photos/album') != -1:
            ids = re.findall(r'/album/(\d+)', link)
            self.album_id = ids[0]
            return link

        # link is a link of an online activity
        m = re.match(PATTERN_ONLINE, link)
        if m:
            resp = requests.get(m.group(0), headers=self.headers)
            link_matched = re.findall(PATTERN_ONLINE_ALBUM, resp.text)
            self.link_type = 'online'
            return link_matched[0]

        # link is a link of a photo in an album
        # http://www.douban.com/photos/photo/2273288058/
        resp = requests.get(link, headers=self.headers)
        link_matched = re.findall(PATTERN_BACK_TO_ALBUM, resp.text)
        if link_matched:
            ids = re.findall(r'/album/(\d+)', link_matched[0])
            self.album_id = ids[0]
            return link_matched[0].split('?')[0]
        self.alert(ERROR_NOT_A_VALID_PIC)
        return ""

    def get_photo_links(self, album_link):
        self.photo_links = []
        page_links = self._get_album_page_links(album_link)
        self.parent_msg(MSG_GET_PIC)
        for link in page_links:
            self.run(self.get_photo_link, link)
        self.parent_msg(MSG_GET_PIC_OK)
        self.photo_links = set(self.photo_links)
        self.alert(MSG_GET_PIC_COUNT.format(len(self.photo_links)))
        return self.photo_links

    def get_photo_link(self, link):
        logging_entry.info("Current album page link: {}".format(link))
        resp = requests.get(link, headers=self.headers)
        photo_url_matched = re.findall(PATTERN_PHOTO_URL, resp.text)
        for url in photo_url_matched:
            url = url.replace("thumb", "photo")
            self.parent_msg(u"获得{}".format(url))
            self.photo_links.append(url)

    def _get_album_page_links(self, album_link):
        self.parent_msg(u"开始获取分页地址")
        logging_entry.info("Start to get page links.")
        links = []
        if self.link_type == 'widget':
            page_content_count = 30
        elif self.link_type == 'online':
            page_content_count = 90
        elif self.link_type == 'album':
            page_content_count = 18
        photo_count = self.run(self._get_photo_page_count, album_link)
        for i in range(photo_count / page_content_count + 1):
            page_url = "{}?start={}".format(album_link, i * page_content_count)
            links.append(page_url)
        return links

    def _get_photo_page_count(self, album_link):
        self.parent_msg(u"开始获取相册图片数量")
        logging_entry.info("Start to get the photo count of an album.")
        resp = requests.get(album_link, headers=self.headers)
        counts = re.findall(PATTERN_PHOTO_COUNT, resp.text)
        if counts:
            logging_entry.info("Album photo count: {}".format(counts[0]))
            return int(counts[0])
        self.alert(ERROR_NOT_GET_PHOTO_COUNT)
        return 0

    def generate_txt(self, links):
        filename_base = time.strftime("%Y%m%d-%H%M%S")
        with open("{}.txt".format(filename_base), "w") as f:
            for line in links:
                f.write(line)
                f.write("\n")
        with open("{}_large.txt".format(filename_base), "w") as f:
            for line in links:
                line = line.replace("/photo/photo/public", "/photo/large/public")
                f.write(line)
                f.write("\n")
        return filename_base

    def alert(self, message):
        print message

    def parent_msg(self, message):
        print message
