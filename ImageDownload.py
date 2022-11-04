# -*- coding: UTF-8 -*-
import os
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup


class ImageDownload(object):

    def __init__(self):
        self.tag = "ImageDownload"
        self.head = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/106.0.0.0 Safari/537.36 ",
            "referer": "https://www.doutub.com/"
        }

    def log(self, log):
        print(self.tag, log)

    def ask_url(self, url):
        req = urllib.request.Request(url = url, headers = self.head)
        html = ""
        try:
            response = urllib.request.urlopen(req)
            html = response.read()
        except Exception as result:
            self.log(result)
        return html

    def parse_img(self, url):
        imglink = re.compile(r'img alt="(.*?)" data-src="(.*?)"', re.S)
        html = self.ask_url(url)
        bs = BeautifulSoup(html, "html.parser")
        names = []
        srcs = []
        # 找到所有的img标签
        for item in bs.find_all('img'):
            item = str(item)
            # 根据上面的正则表达式规则把图片的src以及图片名拿下来
            imgsrc = re.findall(imglink, item)
            # 这里是因为拿取的img标签可能不是我们想要的，所以匹配正则规则之后可能返回空值，因此判断一下
            if (len(imgsrc) != 0):
                imgname = ""
                if imgsrc[0][0] != '':
                    imgname = imgsrc[0][0] + self.get_file_type(imgsrc[0][1])
                else:
                    imgname = self.get_file_name(imgsrc[0][1])
                names.append(imgname)
                srcs.append(imgsrc[0][1])
                self.log(imgname)
                self.log(imgsrc[0][1])
        return names, srcs

    def get_file_type(self, url):
        index = str(url).rfind('.')
        return str(url)[index:]

    def get_file_name(self, url):
        index = str(url).rfind('/')
        return str(url)[index:]

    def download_img(self, img_name, img_url):
        os.makedirs('./img/', exist_ok=True)
        r = requests.get(img_url, headers=self.head)
        with open('./img/{}'.format(img_name), "wb") as f:
            f.write(r.content)

    def start(self, url):
        names, srcs = self.parse_img(url)
        for j in range(len(names)):
            self.download_img(names[j], srcs[j])
