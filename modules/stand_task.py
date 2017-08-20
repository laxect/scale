import gevent


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

    def _handle(self, target):
        return 'helloworld'

    def _run(self, targets):
        return self._handle(targets)

    def run(self, mail_service, targets, inbox=None):
        res = self._run(targets)
        for item in res:
            if item:
                msg_pack = {}
                msg_pack['msg'] = item
                msg_pack['from'] = self.id
                msg_pack['send_to'] = self.send_to
                mail_service.put(msg_pack)


class service(task):
    def _msg_handle(self, msg):
        print(msg)

    def _inbox_service(self, inbox):
        while True:
            item = inbox.get()
            self._msg_handle(item['msg'])

    def _run(self, mail_service=None, targets=None):
        msg_pack = {}
        msg_pack['msg'] = 'hello world'
        msg_pack['from'] = self.id
        msg_pack['send_to'] = self.send_to
        mail_service.put(msg_pack)

    def run(self, mail_service=None, targets=None, inbox=None):
        pool = [
            gevent.spawn(self._run, mail_service, targets),
            gevent.spawn(self._inbox_service, inbox)
        ]
        gevent.joinall(pool)
