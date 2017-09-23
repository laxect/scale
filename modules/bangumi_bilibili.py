import re
import gevent
import requests
import datetime
from lxml import etree
from gevent import queue
# my module template
import standard_task


class bangumi_spider(standard_task.task):
    def __init__(self, targets=None):
        super().__init__()
        self.id = 'laxect.bangumi_spider'
        self.version = 1
        self.send_to = 'laxect.bilibili_spider'

    def _search_bangumi(self, pages, res, url_cnt):
        def next_url(keyward):
            return f'https://search.bilibili.com/all?keyword={keyward}'
        for i in range(url_cnt):
            page = pages.get()
            if page:
                page.encoding = 'utf-8'  # use utf-8 as default encoding
                html = etree.HTML(page.text)
                search = html.xpath('//h3/a[@class="l"]')
                keywards = [item.text for item in search]
                res.extend([next_url(keyward) for keyward in keywards])

    def _search_bilibili(self, pages, res, url_cnt):
        def next_url(bangumi_no):
            return f'https://bangumi.bilibili.com/jsonp/seasoninfo/{bangumi_no}\
.ver?callback=seasonListCallback'
        for i in range(url_cnt):
            page = pages.get()
            if page:
                # find all bangumi no
                bnos = re.findall('\/anime\/(\d+)', page.text)
                bnos = list(set(bnos))  # unique the list
                res.extend([next_url(bno) for bno in bnos])

    def _bilibili_page(self, pages, res, url_cnt):
        CST = datetime.timezone(datetime.timedelta(hours=8), 'CST')
        for i in range(url_cnt):
            page = pages.get()
            if page:
                cal = re.findall('\d+-\d+-\d+', page.text)
                # detect if the bangumi was updated in 14 days.
                if cal:
                    # time that bangumi least updated.
                    year, month, day = [int(date) for date in cal[0].split('-')]
                    least_date = datetime.datetime(year, month, day, tzinfo=CST)
                    # time now.
                    delta = datetime.datetime.now(CST) - least_date
                    if delta < datetime.timedelta(days=14):
                        res.append(re.findall('\/anime\/(\d+)', page.text)[0])

    def _run(self, targets):
        def _bangumi_url(target):
            return [
                f'https://bgm.tv/anime/list/{target}/do',
                f'https://bgm.tv/anime/list/{target}/wish'
            ]

        # the packaged request func.
        def _get_page(urls, pages):
            for url in urls:
                if url:
                    try:
                        pages.put(requests.get(url, timeout=5))
                    except requests.exceptions.RequestException:
                        pages.put(None)
                        continue
                    gevent.sleep(1)
        urls = []
        for target in targets:
            if target:
                urls.extend(_bangumi_url(target=target))
        handle_functions = [
                        self._search_bangumi,
                        self._search_bilibili,
                        self._bilibili_page
        ]
        res = []
        pages = queue.Queue()
        for func in handle_functions:
            res = []
            pools = [gevent.spawn(_get_page, urls, pages)]
            pools.append(gevent.spawn(func, pages, res, len(urls)))
            gevent.joinall(pools)
            urls = res
        return [res]


def mod_init(targets=None):
    return bangumi_spider(targets=targets)
