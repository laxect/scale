import sys
import sqlite3
from gevent.lock import Semaphore


class database():
    _lock = Semaphore(1)
    # object lock

    'laxect.database.3.2.0'
    # used to name as config_date
    def __init__(self, sid='config'):
        self.id = 'laxect.database'
        self._id = sid.replace('.', '_')
        # use for database table name
        self.path = sys.path[0]+'/'+self.id+'.tmp'
        self.sessions = {}
        # use for config
        self.status = False

        self._init_check()

    def _init_check(self):
        database._lock.acquire()
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            try:
                cur.execute(f'select * from {self._id}')
            except sqlite3.OperationalError:
                self._init_table()
        database._lock.release()

    def _init_table(self):
        database._lock.acquire()
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(f'create table {self._id} (key text, value text)')
        database._lock.release()

    def loads(self):
        'load sessions from database.'
        database._lock.acquire()
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(f'select * from {self._id}')
            sessions = cur.fetchall()
        for key, values in sessions:
            exec(f"self.sessions['{key}'] = {values}")
        database._lock.release()
        return self.sessions

    def new_session(self, key, values):
        print(values)
        database._lock.acquire()
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            sql = f'''insert into {self._id} values('{key}', "{values}")'''
            cur.execute(sql)
        database._lock.release()

    # design for common usage.
    def __enter__(self):
        database._lock.acquire()
        self.conn = sqlite3.connect(self.path)
        self.status = True
        return self

    def check_up_to_date(self, cid, content):
        if not self.status:
            raise RuntimeError('Error: status not correct.')
        cur = self.conn.cursor()
        try:
            cur.execute(f"select value from '{self._id}' where key='{cid}'")
        except sqlite3.OperationalError:
            self._init_table()
        res = cur.fetchall()
        if res and res[0][0] == content:
            return False
        cur.execute(
            f"""insert into {self._id} values("{cid}", "{content}")"""
            )
        return True

    def __exit__(self, exc_ty, exc_val, tb):
        self.conn.commit()
        self.conn.close()
        database._lock.release()
        self.status = False


def main():
    test = database()
    print(test.loads())


if __name__ == '__main__':
    main()