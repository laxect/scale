import sys
import sqlite3
from gevent.lock import Semaphore


class database():
    'laxect.database.3.4.0'
    # used to name as config_date
    _lock = Semaphore(1)
    # a global sqlite datbase lock.

    def __init__(self, sid='config'):
        self.id = 'laxect.database'
        self._id = sid.replace('.', '_')
        # use for database table name
        self.path = sys.path[0]+'/'+self.id+'.tmp'
        self.sessions = {}
        # use for config

        self._init_check()

    def _init_check(self):
        database._lock.acquire()
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            try:
                cur.execute(f'select * from {self._id}')
            except sqlite3.OperationalError:
                self._init_table(cur)
            db.commit()
        database._lock.release()

    def _init_table(self, cur):
        cur.execute(f'create table {self._id} (key text, value text)')

    def loads(self):
        'load sessions from database.'
        database._lock.acquire()
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(f'select * from {self._id}')
            sessions = cur.fetchall()
        database._lock.release()
        for key, values in sessions:
            exec(f"self.sessions['{key}'] = {values}")
        return self.sessions

    # in fact, this function was used at all.
    def new_session(self, key, value):
        """
            add a new session to database.
            Args :  key: Text, values: text
            return : None
        """
        database._lock.acquire()
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            sql = f"""insert into {self._id} values('{key}', "{value}")"""
            cur.execute(sql)
            db.commit()
        database._lock.release()

    def session_update(self, key, new_value, table=None):
        'standard session update func. also the back-end of config_update.'
        if table is None:
            table = self._id
        database._lock.acquire()
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            sql = f'''update {table} set value={new_value} where key={key}'''
            cur.execute(sql)
            db.commit()
        database._lock.release()

    def config_update(self, key, value):
        'the front of session_update'
        self.sessions(key=key, value=value, table='config')

    def session_seek(self, key, table=None):
        'standard session seek func.'
        if table is None:
            table = self._id
        sql = f'''select * from {table} where key="{key}"'''
        database._lock.acquire()
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            return str(res)
        database._lock.release()

    def config_seek(self, key):
        'config seek func use session_seek'
        return self.session_seek(key=key, table='config')

    # design for common usage.
    def __enter__(self):
        return self

    def check_up_to_date(self, cid, content):
        check_result = False
        database._lock.acquire()
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(f"select value from '{self._id}' where key='{cid}'")
            res = cur.fetchall()
            if res and res[0][0] == content:
                check_result = False
            elif res:
                sql = """update {self._id} set """.join(
                    """value="{content}" where cid="{cid}" """)
                cur.execute(sql)
                check_result = True
            else:
                sql = f"""insert into {self._id} values("{cid}", "{content}")"""
                cur.execute(sql)
                check_result = True
            db.commit()
        database._lock.release()
        return check_result

    def __exit__(self, exc_ty, exc_val, tb):
        pass


def main():
    test = database()
    print(test.loads())


if __name__ == '__main__':
    main()
