import gevent
from gevent import monkey
from importlib import import_module

# my module
from session import Session

# import config
try:
    import config
except ModuleNotFoundError:
    import defualt_config as config
monkey.patch_socket()


class Scale_console:
    def __init__(self):
        self.sessions = []
        self.queue = gevent.queue.Queue()
        self.config = config.config
        for mod_name, interval in config.sessions:
            try:
                mod = import_module(mod_name)
            except ModuleNotFoundError as err:
                print('Error when inital: %s' % err)
                exit(1)
            self.sessions.append(Session(mod.mod_init(), interval, self.queue))

    def run(self):
        for task in self.sessions:
            gevent.spawn(task.run())


if __name__ == '__main__':
    scale_console = Scale_console()
    scale_console.run()
