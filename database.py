import ast
import sys
import sqlite3


# status code list
uninital = -1
up_to_date = 0
out_of_date = 1


class database():
    def __init__(self):
        self.path = sys.path[0]+'/'+'laxect.database.tmp'
        # TODO need to update sessions tp auto-update in the future.
        # be ware of that the sessions will not update automately now.
        # each item in sessions is a dict
        self.session = {}
        self.status_table = {}  # store the status of each table

    def load(self, table, db):
        '''
        get the content of table in database
        '''
        # cause that up_to_date is 0, so any val that is True IS NOT up_to_date
        if table not in self.session or self.status_table.get(table):
            self._load_table(table, db)
        return self.session[table]

    def _load_table(self, table, db, switch=False):
        '''
        load data into session
        table: str the name of table you want to load
        db: a sqlite3 db object
        switch: use ast to switch or not
        '''
        cur = db.cursor()
        try:
            # clean the old content
            del self.session[table]
            self.session[table] = {}
            # select data from db
            cur.execute(f'select * from {table}')
            origin_date = cur.fetchall()
            for key, value in origin_date:
                if switch:
                    self.session[table][key] = ast.literal_eval(value)
                else:
                    self.session[table][key] = value
        except sqlite3.OperationalError:
            # once if there is not table
            cur.execute(f'create table {table} (key text, value text)')
            db.commit()
        self.status_table[table] = up_to_date

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
