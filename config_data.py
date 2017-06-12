import sys
import sqlite3


class config_data():
    'laxect.config_data.1.0.0'
    # the default config for scale v2.0.0
    def __init__(self):
        self.id = 'laxect.config_data'
        self._id = 'config'  # use for database table name
        self.path = sys.path[0]+'/'+self.id+'.tmp'
        self.sessions = []
        self._init_check()

    def _init_check(self):
        db = sqlite3.connect(self.path)
        cur = db.cursor()
        try:
            cur.execute(f'select * from {self._id}')
        except sqlite3.OperationalError:
            self._init_table()
        db.close()

    def _init_table(self):
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(f'create table {self._id} (key text, value text)')

    def loads(self):
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(f'select * from {self._id}')
            sessions = cur.fetchall()
        for key, values in sessions:
            exec(f'self.sessions[key] = {values}')


def main():
    test = config_data()
    print(test.loads())


if __name__ == '__main__':
    main()
