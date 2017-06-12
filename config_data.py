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
            cur.execute(f'select * from config')
        except sqlite3.OperationalError:
            self._init_check()
        db.close()

    def _init_table(self):
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(f'create table {self._id} (key text, value text)')

    def loads(self):
        db = sqlite3.connect(self.path)
        cur = db.cursor()
        cur.execute('select * from config')
        self.sessions = cur.fetchall()
