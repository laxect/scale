import gevent


class Session:
    'the standard session for all type of task'
    def __init__(self, obj, interval, queue):
        self.obj = obj
        self.queue = queue
        self.interval = interval

    def run(self):
        while True:
            self.obj.run(self.queue)
            gevent.sleep(self.interval)
