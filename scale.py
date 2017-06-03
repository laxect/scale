import gevent
from gevent import monkey, queue
from importlib import import_module

# my module
from session import Session

# import config
try:
    import config
except ModuleNotFoundError:
    import default_config as config
monkey.patch_all()


class Scale_console:
    def __init__(self):
        self.sessions = []
        self.queue = queue.Queue()
        for mod_name in config.sessions:
            interval = config.sessions[mod_name]
            try:
                mod = import_module(mod_name)
            except ModuleNotFoundError as err:
                print('Error when inital: %s' % err)
                exit(1)
            self.sessions.append(Session(mod.mod_init(), interval, self.queue))
        print('scale inital complete.')

    def run(self):
        'run task'
        pool = [gevent.spawn(task.run) for task in self.sessions]
        gevent.joinall(pool)


if __name__ == '__main__':
    scale_console = Scale_console()
    scale_console.run()
