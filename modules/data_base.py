# the alternative for store_file
import sys
import sqlite3
import hashlib


class data_base():
    # laxect.data_base.1.0.0
    def __init__(self, sid):
        self.sid = sid.replace('.', '_')
        self.status = False
        self.path = sys.path[0] + '/laxect.data_base.tmp'
        self.hash = hashlib.new('ripemd160')

    def _table_build_up(self):
        cur = sqlite3.connect(self.path).cursor()
        cur.execute(f'create table {self.sid} (id text, hash text)')

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.status = True
        return self

    def check_up_to_date(self, cid, content):
        if not self.status:
            raise RuntimeError('Error: status not correct.')
        cur = self.conn.cursor()
        try:
            cur.execute(f'select hash from \'{self.sid}\' where id=\'{cid}\'')
        except sqlite3.OperationalError:
            self._table_build_up()
        res = cur.fetchall()
        if res:
            return False
        self.hash.update(str(content).encode('utf-8'))
        _hash = self.hash.hexdigest()
        cur.execute(f'insert into {self.sid} values(\'{cid}\', \'{_hash}\')')
        return True

    def __exit__(self, exc_ty, exc_val, tb):
        self.conn.commit()
        self.conn.close()
        self.status = False
