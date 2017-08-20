import re
import requests
from modules import database
from . import stand_task


class light_novel_spider(stand_task.task):
    def __init__(self, keywards):
        self.id = 'laxect.light_novel_spider'
        self.version = 1
        self.keywards = keywards
        self.url = 'https://www.lightnovel.cn/forum-173-1.html'

    def _format_item(self, cid, text, status):
        msg = re.findall('xst\">(.*)</a>', text)[0]
        url = f'https://www.lightnovel.cn/thread-{cid}-1-1.html'
        if status == '中':
            fmsg = f'轻之国度 新开启的主题:\n{msg}\n{url}'
        else:
            fmsg = f'轻之国度 主题进度100%:\n{msg}\n{url}'
        return fmsg

    def _handle(self, text):
        # the standard handle of spider
        res = []
        for keyward in self.keywards:
            pattern = re.findall('.*'+keyward+'.*', text)
            with database.database(self.id) as db:
                for item in pattern:
                    cid = re.findall('thread-(\d+)-1-1', item)[0]
                    content = re.findall('中|完成', item)[0]
                    if db.check_up_to_date(cid, content):
                        res.append(self._format_item(cid, item, content))
        return res

    def _run(self, keywards=None):
        if keywards:
            self.keywards = keywards
        try:
            return self._handle(requests.get(self.url).text)
        except requests.exceptions.RequestException as err:
            return []


def mod_init(keywards):
    return light_novel_spider(keywards)


if __name__ == '__main__':
    class test_queue:
        def put(self, obj):
            print(obj)
    keywards = ['和ヶ原聡司', '久遠侑']
    lns = mod_init(keywards)
    lns.run(test_queue())
