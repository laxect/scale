import re
import json
import gevent
import requests
from . import stand_task

# my module
from modules import database


class bilibili_spider(stand_task.task):
    'a spider espeacially design for bilibili bangumi'
    def __init__(self, aim=None):
        'aim in stand of which bangumi you want to watch'
        super().__init__()
        self.id = 'laxect.bilibili_spider'
        self.version = 1

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
        fres = '%s 更新了第%s集 %s\n%s' % res  # format string
        with database.database(self.id) as db:
            if db.check_up_to_date(aim, str(res)):
                return fres
        return None

    def _aim_run(self, aim, res):
        try:
            tres = self._handle(requests.get(self._url(aim)).text, aim)
        except requests.exceptions.RequestException as err:
            return
        if tres:
            res.append(tres)

    def _run(self, aims):
        res = []
        pool = []
        for aim in aims:
            pool.append(gevent.spawn(self._aim_run, aim, res))
        gevent.joinall(pool)
        return res


def mod_init(aim):
    return bilibili_spider(aim=aim)
