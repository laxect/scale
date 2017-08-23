import gevent
from pprint import pprint
from gevent import monkey, queue
from importlib import import_module

# my module
from modules import database
monkey.patch_all(aggressive=True)
# use for format output.
div_line = '=================='
div_line2 = '------------------'


class scale_console:
    def __init__(self, debug=False):
        self.debug = debug  # the debug mode and the release mode.
        self.sessions = []  # include all task and service need to run.
        self.inbox = queue.Queue()
        self.inbox_table = {}
        # load the config from database.
        self.config = database.database(sid='config', debug=debug)
        self.config.loads()
        if self.debug:
            self.config.sessions = {
                'bangumi_bilibili': (1500, ('laxect_cn',)),
                'bilibili_spider': (1200, ('1071',)),
                'lightnovel_spider': (1500, (
                    '和ヶ原聡司', '久遠侑', '七沢またり', '白鸟士郎',
                    '羊太郎', '入间人间', '十文字青', '葵せきな',
                )),
                'scales_bot': (0, (
                    '268094147:AAHNDBMmFQQaUqVm6mfaCe0a9uFmXWIiVBk', 290809873
                )),
                'timer': (0, ())
            }  # test date.
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
                mod_name = mod_name.split('.')[0]
                mod = import_module('modules.'+mod_name)
            except ImportError as err:
                print('Error when inital: %s' % err)
                exit(1)
            # add module into run queue.
            task_obj = mod.mod_init(argv)
            task_inbox = None
            if task_obj.inbox:
                if task_obj.inbox not in self.inbox_table:
                    self.inbox_table[task_obj.inbox] = queue.Queue()
                task_inbox = self.inbox_table[task_obj.inbox]
            self.sessions.append(gevent.spawn(
                self.task_run, mod_name, task_obj, inte, self.inbox, task_inbox
            ))
            self.sessions.append(gevent.spawn(self._scale_inbox_service))

    def _scale_inbox_service(self):
        while True:
            mail = self.inbox.get()
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

    def task_run(self, task_id, task_obj, inte, system_inbox, task_inbox=None):
        count = 0
        while True:
            self.config.loads()
            task_obj.run(
                mail_service=system_inbox,
                targets=self.config.sessions[task_id][1],
                inbox=task_inbox,
                debug=self.debug
            )
            if self.debug:
                count += 1
                if count >= 3:
                    return
                gevent.sleep(60)
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
