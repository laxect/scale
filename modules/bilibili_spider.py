import re
import json
import gevent
import requests
from gevent.queue import Empty

# my module
from . import stand_task
from modules import database


class bilibili_spider(stand_task.task):
    'a spider espeacially design for bilibili bangumi'
    def __init__(self, aim=None):
        'aim in stand of which bangumi you want to watch'
        super().__init__()
        self.id = 'laxect.bilibili_spider'
        self.inbox = self.id
        self.version = 1
        self.mode = 'from_database'
        self.aims = []

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
            ts = self._handle(requests.get(self._url(aim), timeout=5).text, aim)
        except requests.exceptions.RequestException as err:
            return
        if ts:
            res.append(ts)

    def _run(self, targets):
        if self.mode == 'from_inbox':
            aims = self.aims
        else:
            aims = targets
        res = []
        pool = []
        for aim in aims:
            if aim:
                pool.append(gevent.spawn(self._aim_run, aim, res))
        gevent.joinall(pool)
        if self.debug:
            msg = f'the res of run is:\n{str(res)}'
            self.debug_information_format(msg)
        return res

    def _inbox_handle(self, inbox):
        aims = []
        try:
            while True:
                item = inbox.get(block=False)
                if item:
                    aims = item['msg']
        except Empty:
            pass
        if self.debug:
            msg = f'the argv recv from inbox is:\n{str(aims)}'
            self.debug_information_format(msg)
        if aims:
            self.aims = aims
            self.mode = 'from_inbox'


def mod_init(aim):
    return bilibili_spider(aim=aim)
