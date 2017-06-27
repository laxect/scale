# will be renamed as database in no time.
import sys
import sqlite3


class database():
    'laxect.database.2.0.0'
    def __init__(self, sid='config'):
        self.id = 'laxect.database'
        self._id = sid
        # use for database table name
        self.path = sys.path[0]+'/'+self.id+'.tmp'
        self.sessions = {}
        self._init_check()

    def _init_check(self):
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            try:
                cur.execute(f'select * from {self._id}')
            except sqlite3.OperationalError:
                self._init_table()

    def _init_table(self):
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(f'create table {self._id} (key text, value text)')

    def loads(self):
        'load sessions from database.'
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(f'select * from {self._id}')
            sessions = cur.fetchall()
        for key, values in sessions:
            exec(f"self.sessions['{key}'] = {values}")
        return self.sessions

    def new_session(self, key, values):
        print(values)
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            sql = f'''insert into {self._id} values('{key}', "{values}")'''
            cur.execute(sql)


def main():
    test = database()
    print(test.loads())


if __name__ == '__main__':
    main()
