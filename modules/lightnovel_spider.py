import re
import requests
from modules import database
from . import stand_task


class light_novel_spider(stand_task.task):
    def __init__(self, keywards=None):
        super().__init__()
        self.id = 'laxect.light_novel_spider'
        self.version = 1
        self.url = 'https://www.lightnovel.cn/forum-173-1.html'

    def _format_item(self, cid, text, status):
        msg = re.findall('xst\">(.*)</a>', text)[0]
        url = f'https://www.lightnovel.cn/thread-{cid}-1-1.html'
        if status == '中':
            fmsg = f'轻之国度 新开启的主题:\n{msg}\n{url}'
        else:
            fmsg = f'轻之国度 主题进度100%:\n{msg}\n{url}'
        return fmsg

    def _handle(self, text, keywards):
        # the standard handle of spider
        res = []
        for keyward in keywards:
            pattern = re.findall('.*'+keyward+'.*', text)
            with database.database(self.id) as db:
                for item in pattern:
                    cid = re.findall('thread-(\d+)-1-1', item)[0]
                    content = re.findall('中|完成|转载', item)
                    if content and db.check_up_to_date(cid, content[0]):
                        res.append(self._format_item(cid, item, content[0]))
        return res

    def _run(self, keywards=None):
        try:
            return self._handle(requests.get(self.url).text, keywards)
        except requests.exceptions.RequestException as err:
            return []


def mod_init(keywards):
    return light_novel_spider(keywards)
