import ast
import sys
import sqlite3


class database():
    # status code list
    uninital = -1
    up_to_date = 0
    out_of_date = 1

    def __init__(self, inbox, mail_service):
        # use inbox to recvive request and return res
        self.inbox = inbox
        self.mail_service = mail_service
        self.path = sys.path[0]+'/'+'laxect.database.tmp'
        # TODO need to update sessions tp auto-update in the future.
        # be ware of that the sessions will not update automately now.
        # each item in sessions is a dict
        self.session = {}
        self.status_table = {}  # store the status of each table
        # the action table
        # low level apis
        self.action_table = {
            'get': 'select * from {table} where key="{key}"',
            'put': 'insert into {table} values("{key}", "{value}")',
            'delete': 'delete from {table} where key="{key}"',
            'update': 'update {table} set value="{value}" where key="{key}"',
        }

    def load(self, table, db, switch=False):
        '''
        load data into session
        table: str the name of table you want to load
        db: a sqlite3 db object
        switch: use ast to switch or not
        '''
        # cause that up_to_date is 0, so any val that is True IS NOT up_to_date
        # with no val link with key(table) dict.get will return None in defualt
        if table not in self.session or self.status_table.get(table):
            cur = db.cursor()
            # switch patch
            # only config table need switch now
            if table == 'config':
                switch = True
            try:
                # clean cache
                self.session[table] = {}
                # select data from db
                cur.execute(f'select * from {table}')
                for key, value in cur.fetchall():
                    if switch:
                        self.session[table][key] = ast.literal_eval(value)
                    else:
                        self.session[table][key] = value
            except sqlite3.OperationalError:
                # once if there is not table
                cur.execute(f'create table {table} (key text, value text)')
                db.commit()
            self.status_table[table] = database.up_to_date
        return self.session[table]

    def action(self, db, act, table, key, val=None):
        if act in self.action_table:
            sql = self.action_table[act].format(table=table, key=key, value=val)
            cur = db.cursor()
            cur.execute(sql)
            self.status_table[table] = database.out_of_date  # update the st tb
            return cur.fetchall()

    def data_service(self):
        while True:
            mail = self.inbox.get()
