import gevent
from gevent import monkey, queue
from importlib import import_module

# my module
from session import Session

# import config
from modules import database
monkey.patch_all(aggressive=True)


class Scale_console:
    def __init__(self):
        self.sessions = []
        self.queue = queue.Queue()

        config = database.database()
        cons = config.loads()
        from pprint import pprint
        pprint(cons)
        for mod_name in config.sessions:
            inte, argv, *_ = config.sessions[mod_name]
            try:
                mod_name = mod_name.split('.')[0]
                mod = import_module('modules.'+mod_name)
            except ImportError as err:
                print('Error when inital: %s' % err)
                exit(1)
            self.sessions.append(Session(mod.mod_init(argv), inte, self.queue))
        print('scale inital complete.')

    def run(self):
        'run task'
        pool = [gevent.spawn(task.run) for task in self.sessions]
        gevent.joinall(pool)


if __name__ == '__main__':
    scale_console = Scale_console()
    try:
        scale_console.run()
    except KeyboardInterrupt:
        print('Good Bye.')
