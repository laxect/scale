import gevent
from gevent import queue
from gevent import monkey
from pprint import pprint
from importlib import import_module
# my modules
from modules import database
# monkey patch for gevent.
monkey.patch_all(aggressive=True)


class scale_console:
    def __init__(self):
        self.sessions = []  # include all task and service need to run.
        # the mail service
        self.inbox_table = {}
        self.inbox = queue.Queue()
        # load the config from database or from config(argv).
        # the config load from database.
        self.config = database.database(sid='config')
        self.config.loads()
        pprint(self.config.sessions)
        # inital all task
        self.tasks_init(self.config.sessions)
        # add the mail service into run queue
        self.sessions.append(gevent.spawn(self.scale_inbox_service))
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
            # create all of task.
            task_obj = mod.mod_init(mail_service=self.inbox)
            # the inital of task inbox
            if task_obj.inbox_tag:
                task_inbox = queue.Queue()
                for tag in task_obj.inbox_tag:
                    self.inbox_table.setdefault(tag, [])
                    self.inbox_table[tag].append(task_inbox)
            task_obj.initalize(inbox=task_inbox)
            # add all task into run queue.
            self.sessions.append(gevent.spawn(task_obj.run))

    def scale_inbox_service(self):
        'standard mail service of scale'
        while True:
            mail = self.inbox.get()
            sendto = mail['send_to']
            if sendto in self.inbox_table:
                self.inbox_table[sendto].put(mail)

    def run(self):
        'run task'
        gevent.joinall(self.sessions)


if __name__ == '__main__':
    scales = scale_console()
    try:
        scales.run()
    except KeyboardInterrupt:
        print('Good Bye.')
