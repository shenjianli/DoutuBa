import os.path
import re

import requests


class BiaoQing(object):
    def __init__(self):
        self.TAG = "BiaoQing"
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }

    def log(self, log):
        print(self.TAG, log)

    def start(self):
        url = 'https://fabiaoqing.com/biaoqing/lists/page/1.html'
        response = requests.get(url, headers=self.headers)
        # self.log(response.text)
        re_data = re.findall('<img class="ui image lazy" data-original="(.*?)" src="/Public/lazyload/img/transparent.gif" title="(.*?)"', response.text)
        self.log(re_data)
        for img in re_data:
            link = img[0]
            suffix = link.split('.')[-1]
            title = img[1]
            title = re.sub(r'[\/:*?" @<>|]?', '', title)
            self.log("开始下载 {}".format(title))
            content = requests.get(link, headers=self.headers).content
            file = f'img/'
            if not os.path.exists(file):
                os.makedirs(file)
            with open('img/' + title + "." + suffix, 'wb') as file:
                file.write(content)


if __name__ == '__main__':
    biaoqing = BiaoQing()
    biaoqing.start()