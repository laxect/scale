import sys
import sqlite3


class database():
    def __init__(self, sid='config'):
        self._id = sid.replace('.', '_')  # use for database table name
        self.path = sys.path[0]+'/'+self.id+'.tmp'
        # be ware of that the sessions will not update automately.
        self.sessions = {}
        # func action table.
        self.action_table = {
            'new': self.new_session,
            'seek': self.session_seek,
            'update': self.session_update,
        }

    # check if the table is exist.
    def _init_check(self):
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            try:
                cur.execute(f'select * from {self._id}')
                cur.fetchall()
            except sqlite3.OperationalError:
                self._init_table(cur)
                db.commit()

    # be warn of that this func will NOT acquire for lock.
    def _init_table(self, cur):
        cur.execute(f'create table {self._id} (key text, value text)')

    # loads config from database.
    # return a dict contains config.
    def loads(self):
        'load sessions from database.'
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(f'select * from {self._id}')
            sessions = cur.fetchall()
        for key, values in sessions:
            exec(f'self.sessions["{key}"] = {values}')
        return self.sessions

    def new_session(self, key, value, table=None):
        '''
            add a new session to database.
            Args :  key: Text, values: text
            return : None
        '''
        table = table if table else self._id
        sql = f'insert into {table} values("{key}", "{value}")'
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(sql)
            db.commit()

    def session_update(self, key, value, table=None):
        'standard session update func. also the back-end of config_update.'
        if not table:
            table = self._id
        sql = f'update {table} set value="{value}" where key="{key}"'
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(sql)
            db.commit()

    def session_seek(self, key, value=None, table=None):
        # look for that this func will not use *value*
        'standard session seek func.'
        if table is None:
            table = self._id
        sql = f'select * from {table} where key="{key}"'
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(sql)
            res = cur.fetchall()
        return res

    # TODO need to de re wrote
    def check_up_to_date(self, cid, content, table=None):
        table = table if table else self._id
        check_result = False
        with sqlite3.connect(self.path) as db:
            cur = db.cursor()
            cur.execute(f'select value from "{self._id}" where key="{cid}"')
            res = cur.fetchall()
            if res and res[0][0] == content:
                check_result = False
            elif res:
                cur.execute(
                    f'update {self._id} set value="{content}" where key="{cid}"'
                )
                check_result = True
            else:
                cur.execute(
                    f'insert into {self._id} values("{cid}", "{content}")'
                )
                check_result = True
            db.commit()
        return check_result

    def commit_handle(self, action, table=None, key=None, value=None):
        '''
        A common port for database usage
        '''
        table = table if table else self._id  # make sure that table isn't empty
        if action in self.action_table:
            return self.action_table[action](key=key, value=value, table=table)
