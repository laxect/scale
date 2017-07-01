import gevent
from modules import database


class Session:
    'the standard session for all type of task'
    def __init__(self, obj, interval, que, id):
        self.db = database.database()
        self.id = id
        self.obj = obj
        self.queue = que
        self.interval = interval

    def run(self):
        while True:
            session = self.db.loads()
            self.obj.run(self.queue, session[self.id][1])
            gevent.sleep(self.interval)
