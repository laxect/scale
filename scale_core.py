import gevent
from gevent import queue
from gevent import monkey
from pprint import pprint
from importlib import import_module
# my modules
from modules import database
# monkey patch for gevent.
monkey.patch_all(aggressive=True)
# use for format output.
div_line = '=================='
div_line2 = '------------------'


class scale_console:
    def __init__(self, debug=False, config=None):
        self.debug = debug  # the debug mode and the release mode.
        self.task_count = 0  # design for debug mode.
        self.sessions = []  # include all task and service need to run.
        self.inbox = queue.Queue()
        self.inbox_table = {}
        # load the config from database.
        self.config = database.database(sid='config', debug=debug)
        self.config.loads()
        if self.debug:
            # load config from test date.
            self.config.sessions = config
        # output the details of config.
        pprint(self.config.sessions)
        # after loads(), the config.sessions contain content.
        self.tasks_init(self.config.sessions)
        print('scale inital complete.')

    def tasks_init(self, config_sessions):
        for mod_name in config_sessions:
            inte, argv, *_ = config_sessions[mod_name]
            # import module.
            try:
                mod = import_module('modules.'+mod_name)
            except ImportError as err:
                print('Error when inital: %s' % err)
                exit(1)
            # add module into run queue.
            task_obj = mod.mod_init(argv)
            task_inbox = None
            # the inital of inbox
            if task_obj.inbox:
                if task_obj.inbox not in self.inbox_table:
                    self.inbox_table[task_obj.inbox] = queue.Queue()
                task_inbox = self.inbox_table[task_obj.inbox]
            self.sessions.append(gevent.spawn(
                self.task_run, mod_name, task_obj, inte, task_inbox
            ))
            self.sessions.append(gevent.spawn(self._scale_inbox_service))

    def _scale_inbox_service(self):
        timeout = 20 if self.debug else False  # debug switch
        while True:
            try:
                mail = self.inbox.get(timeout=timeout)
            except queue.Empty as err:
                if self.task_count == 0:  # for debug using.
                    return
                continue
            if self.debug:
                print(div_line + div_line)
                for key in mail:
                    print(div_line2 + div_line2)
                    print('    ' + str(key) + ' :')
                    print(mail[key])
                    print(div_line2 + div_line2)
                print(div_line + div_line)
            sendto = mail['send_to']
            if sendto in self.inbox_table:
                self.inbox_table[sendto].put(mail)

    def task_run(self, task_id, task_obj, inte, task_inbox=None):
        self.task_count += 1
        count = 0
        while True:
            self.config.loads()
            task_obj.run(
                mail_service=self.inbox,
                targets=self.config.sessions[task_id][1],
                inbox=task_inbox,
                debug=self.debug
            )
            if self.debug:
                count += 1
                if count >= 3:
                    self.task_count -= 1
                    return
                gevent.sleep(10)
            else:
                gevent.sleep(inte)

    def run(self):
        'run task'
        gevent.joinall(self.sessions)


if __name__ == '__main__':
    scales = scale_console()
    try:
        scales.run()
    except KeyboardInterrupt:
        print('Good Bye.')
