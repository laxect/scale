import re
import json
import gevent
import requests
# my module
from modules import database


class bilibili_spider():
    'a spider espeacially design for bilibili bangumi'
    # laxect.bilibili_spider.3.1.0
    def __init__(self, aim):
        'aim in stand of which bangumi you want to watch'
        self._aims = aim
        self.id = 'laxect.bilibili_spider'

    def _id(self, aim):
        return f'laxect.bilibili_spider.{aim}'

    def _url(self, aim):
        url = f'http://bangumi.bilibili.com/jsonp/seasoninfo/{aim}\
.ver?callback=seasonListCallback'
        return url

    def _handle(self, text, aim):
        'the fun to handle the text spider return'
        dica = json.loads(re.findall('\w*\((.*)\);', text)[0])
        title = dica['result']['bangumi_title']
        eps = dica['result']['episodes']
        res = (
            title,
            eps[0]['index'],
            eps[0]['index_title'],
            eps[0]['webplay_url'])
        fres = "%s 更新了第%s集 %s\n%s" % res  # format string
        with database.database(self._id(aim)) as db:
            if db.check_up_to_date(aim, str(res)):
                return (fres, self._id(aim))
        return None

    def _run(self, que, aim):
        res = self._handle(requests.get(self._url(aim)).text, aim)
        if res:
            que.put(res[0])

    def run(self, que):
        'the standard run entry'
        pool = []
        for aim in self._aims:
            pool.append(gevent.spawn(self._run, que, aim))
        gevent.joinall(pool)


def mod_init(aim):
    return bilibili_spider(aim=aim)


if __name__ == '__main__':
    class test_queue:
        def put(self, obj):
            print(obj)

    print(mod_init().run(test_queue()))
