import gevent
import traceback
from gevent.queue import Empty


class task():
    '''
    the stand task module for all module.
    this class realize the inbox system and the log system.
    the 'inbox' tag in behalf of the default inbox of all
    message that doesn't point a specify inbox.
    '''
    def __init__(self, targets=None):
        self.id = 'laxect.task'
        self.send_to = 'inbox'
        self.inbox = None  # design for task need inbox
        self.debug = False

    def _handle(self, target):
        return 'helloworld'

    def _inbox_handle(self, inbox):
        try:
            while True:
                inbox.get(timeout=0)
        except Empty:
            pass

    def _run(self, targets):
        return self._handle(targets)

    def run(self, mail_service, targets, inbox=None, debug=False):
        if debug:
            self.debug = True
        try:
            if inbox:
                self._inbox_handle(inbox)
            res = self._run(targets)
            for item in res:
                if item:
                    msg_pack = {
                        'msg': item,
                        'from': self.id,
                        'send_to': self.send_to,
                    }
                    mail_service.put(msg_pack)
        except Exception as err:
            msg_pack = {
                'msg': f'module {self.id} crashed for\n    {err}',
                'details': traceback.format_exc(),
                'from': self.id,
                'send_to': 'inbox',
            }
            mail_service.put(msg_pack)


class service(task):
    def _msg_handle(self, msg):
        print(msg)

    def _inbox_service(self, inbox):
        while True:
            item = inbox.get()
            self._msg_handle(item['msg'])

    def _run(self, mail_service=None, targets=None):
        msg_pack = {
            'msg': 'helloworld',
            'from': self.id,
            'send_to': self.send_to,
        }
        mail_service.put(msg_pack)

    def run(self, mail_service=None, targets=None, inbox=None):
        pool = [
            gevent.spawn(self._run, mail_service, targets),
            gevent.spawn(self._inbox_service, inbox)
        ]
        gevent.joinall(pool)
