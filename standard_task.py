import gevent
import requests
from gevent import queue


class task():
    '''
    the stand task module for all module.
    this class realize the inbox system and the log system.
    the 'inbox' tag in behalf of the default inbox of all
    message that doesn't point a specify inbox.
    '''
    def __init__(self, mail_service, hooks=None):
        self.id = None
        self.send_to = 'inbox'
        self.mail_service = mail_service
        self.inbox_tag = [self.id]  # design for task need inbox
        self.hooks = hooks  # the hooks system.
        # if u want to use page_get u must set this to True.
        self.page_get_switch = False
        # u should add u service here.
        self.service = []
        self.status = 'stop'  # ['stop', 'run', 'pause', 'broken']

    def initalize(self, inbox=None):
        'use this func to initalize the whole class'
        if self.inbox_tag:
            self.inbox = inbox
            self.scale_api_result = queue.Queue()
            self.service.append(gevent.spawn(self.inbox_service))
        if self.page_get_switch:
            # u shoule put u target into url_que and get result from res_que
            self.page_url_queue = queue.Queue()
            self.page_res_queue = queue.Queue()
            self.service.append(gevent.spawn(self.page_get))
        if self.hooks:
            pass  # design for future

    def gen_msg(self, content, fport='main', send_to=None, metadata=None):
        'generator a mp from metadata'
        # look for that in this version, send_to is a list which len is 2.
        return {
            'msg': content,
            'meme-type': 'text',
            'from': self.id,
            'from_port': fport,
            'send_to': send_to[0] if send_to else self.send_to,
            'send_to_port': send_to[1] if send_to else 'main',
            'metadata': metadata,
        }

    def page_get(self):
        'a standard page get gevenlet'
        while True:
            url = self.page_url_queue.get()
            # use None as EOF
            if not url:
                break
            try:
                page = requests.get(url)
            except requests.exceptions.RequestException:
                # will return None if any Error happened.
                self.page_res_queue.put(None)
            else:
                self.page_res_queue.put(page)

    def inbox_service(self):
        '''
        a service to handle the msg in inbox
        u must write a mail_handle function to use this.
        '''
        if not self.inbox:
            return
        while True:
            msg = self.inbox.get()
            if msg:
                if msg['send_to_port'] == 'sca':
                    self.scale_api_result.put(msg)
                else:
                    self.mail_handle(msg)
            else:
                break

    # BUG will *NOT* fix in next few generations
    # look for: if your ask for more than one api in the same time,
    # the result will not return in order
    def scale_core_apis(self, api, args=None):
        '''
        u should use this function to ask scale_apis
        need inbox to work proprely.
        args should be a list.
        '''
        sa_add = ['scale_api', api]
        self.mail_service.put(self.gen_msg(args, fport='sca', send_to=sa_add))
        return self.scale_api_result.get()

    def run(self):
        def run_steps():
            # if you want to do some thing, you should put your action in _run
            if not self._run():
                print('no run func assigned.')
                print(self.id)
                return
            while True:
                self.status = 'run'
                self._run()
                self.status = 'pause'
                # gevent.sleep(inte)
        pools = self.service
        pools.append(gevent.spawn(run_steps))
        gevent.joinall(pools)
