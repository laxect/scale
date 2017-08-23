import re
import gevent
import requests
import datetime
from lxml import etree
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
        url = f'https://bangumi.bilibili.com/jsonp/seasoninfo/{bangumi_no}\
.ver?callback=seasonListCallback'
        CST = datetime.timezone(datetime.timedelta(hours=8), 'CST')
        try:
            page = requests.get(url, timeout=5)
        except requests.exceptions.RequestException:
            return
        page.encoding = page.apparent_encoding  # auto detect the encoding
        times = re.findall('\d+-\d+-\d+', page.text)
        times.sort(reverse=True)
        # detect if the bangumi was updated in 14 days.
        if times:
            least_time = times[0]
            year, month, day = [int(date) for date in least_time.split('-')]
            # time that bangumi least updated.
            least_date = datetime.datetime(year, month, day, tzinfo=CST)
            # time now.
            delta = datetime.datetime.now(CST) - least_date
            if delta < datetime.timedelta(days=14):
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
