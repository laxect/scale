import gevent
from gevent import monkey, queue
from importlib import import_module

# my module
from session import Session

# import config
try:
    import config
except ImportError:
    import default_config as config
monkey.patch_all()


class Scale_console:
    def __init__(self):
        self.sessions = []
        self.queue = queue.Queue()
        for mod_name in config.sessions:
            inte = config.sessions[mod_name][0]
            argv = config.sessions[mod_name][1]
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
