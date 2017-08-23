import gevent
import datetime
import traceback
from gevent.queue import Empty
div_line = '=================='
div_line2 = '------------------'


class task():
    '''
    the stand task module for all module.
    this class realize the inbox system and the log system.
    the 'inbox' tag in behalf of the default inbox of all
    message that doesn't point a specify inbox.
    '''
    def __init__(self, targets=None):
        self.id = None
        self.send_to = 'inbox'
        self.inbox = None  # design for task need inbox
        self.debug = False

    def debug_information_format(self, msg):
        'design for standard debug information output'
        print(div_line + div_line)
        print(f'From {self.id}:')
        print(div_line2 + div_line2)
        print(str(msg))
        print(div_line + div_line)

    def gen_msg_pack(self, content, send_to=None, metadata=None):
        'generator a mp from metadata'
        msg_pack = {
            'msg': content,
            'from': self.id,
            'send_to': send_to if send_to else self.send_to,
            'metadata': metadata,
        }
        return msg_pack

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
                    mail_service.put(self.gen_msg_pack(item))
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
        try:
            while True:
                item = inbox.get()
                self._msg_handle(item['msg'])
        except gevent.hub.LoopExit as err:
            pass  # use for debug time.

    def _run(self, mail_service=None, targets=None):
        msg_pack = {
            'msg': 'helloworld',
            'from': self.id,
            'send_to': self.send_to,
        }
        mail_service.put(msg_pack)

    def run(self, mail_service=None, targets=None, inbox=None, debug=False):
        if debug:
            self.debug = True
        pool = [
            gevent.spawn(self._run, mail_service, targets),
            gevent.spawn(self._inbox_service, inbox)
        ]
        gevent.joinall(pool)


class timer(task):
    # you can use this like a simple Alarm.
    def __init__(self, targets=None):
        '''
        the init func for timer.
        nextdate    func        : give the datetime of now, cal the next date.
        once the time nextdate get, it will send msg.
        '''
        super().__init__()
        self.targets = targets
        # remember to redefine the time_zone for your work.
        self.time_zone = datetime.timezone(datetime.timedelta(hours=0), 'UTC')

    def next_time(self, now_time):
        return now_time + datetime.timedelta(seconds=39)

    def action(self, mail_service, targets=None, inbox=None):
        mail_service.put(self.gen_msg_pack('hello world'))

    def run(self, mail_service, targets=None, inbox=None, debug=False):
        if debug:
            self.debug = True
        try:
            now_time = datetime.datetime.now(datetime.timezone.utc)
            # adjust the time zone of now_time.
            now_time.astimezone(self.time_zone)
            next_time = self.next_time(now_time)
            time_sleep = (next_time - now_time).total_seconds()
            if not debug:
                gevent.sleep(time_sleep)
            else:  # the debug test area.
                msg = f'the sleep of time is:\n{time_sleep}'
                self.debug_information_format(msg)
            self.action(mail_service, targets, inbox)
        except Exception as err:
            msg_pack = {
                'msg': f'module {self.id} crashed for\n    {err}',
                'details': traceback.format_exc(),
                'from': self.id,
                'send_to': 'inbox',
            }
            mail_service.put(msg_pack)