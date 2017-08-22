import re
from lxml import etree
import gevent
import requests
# my module template
from . import stand_task


class bangumi_spider(stand_task.task):
    def __init__(self, targets=None):
        super().__init__()
        self.id = 'laxect.bangumi_spider'
        self.version = 1
        self.send_to = 'laxect.bilibili_spider'

    def _bangumi_url(self, target):
        return [
            f'https://bgm.tv/anime/list/{target}/do',
            f'https://bgm.tv/anime/list/{target}/wish'
        ]

    def _search_bangumi(self, url, res):
        try:
            page = requests.get(url, timeout=5)
        except requests.exceptions.RequestException:
            return
        # auto detect encoding.
        page.encoding = page.apparent_encoding
        html = etree.HTML(page.text)
        search = html.xpath('//h3/a[@class="l"]')
        keywards = [item.text for item in search]
        pool = [
                gevent.spawn(self._search_bilibili, keyward, res)
                for keyward in keywards]
        gevent.joinall(pool)

    def _search_bilibili(self, keyward, res):
        url = f'https://search.bilibili.com/all?keyword={keyward}'
        try:
            page = requests.get(url, timeout=5)
        except requests.exceptions.RequestException:
            return
        # auto detect encoding.
        page.encoding = page.apparent_encoding
        html = etree.HTML(page.text)
        search = html.xpath('//a[@class="list sm "]/attribute::href')
        # bangumi numbers.
        bnos = [re.findall('\/anime\/(\d+)', url)[0] for url in search]
        # gevent gevenlet pool.
        pool = [gevent.spawn(self._bilibili_page, bno, res) for bno in bnos]
        gevent.joinall(pool)

    def _bilibili_page(self, bangumi_no, res):
        url = f'https://bangumi.bilibili.com/anime/{bangumi_no}'
        try:
            page = requests.get(url, timeout=5)
        except requests.exceptions.RequestException:
            return
        page.encoding = page.apparent_encoding  # auto detect the encoding
        html = etree.HTML(page.text)
        info_row = html.xpath('//div[@class="info-row info-update"]/em/span')
        judge = False
        for info in info_row:
            if re.findall('连载', info.text):
                judge = True
        if judge:
            res.append(bangumi_no)

    def _run(self, targets=None):
        urls = []
        for target in targets:
            if target:
                urls.extend(self._bangumi_url(target=target))
        res = []
        pool = [gevent.spawn(self._search_bangumi, url, res) for url in urls]
        gevent.joinall(pool)
        return [res]


def mod_init(targets=None):
    return bangumi_spider(targets=targets)
