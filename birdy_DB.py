import sqlite3
from sqlite3 import Error

class Birdy_DB:
    def __init__(self, db_file=r"db/birdy.db"):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        notify_table = """ CREATE TABLE IF NOT EXISTS notifications (
        id integer PRIMARY KEY,
        user_id integer); """

        photos_table = """CREATE TABLE IF NOT EXISTS photos (
        id integer PRIMARY KEY,
        user_id integer);"""
    
        stream_table = """CREATE TABLE IF NOT EXISTS streaming (
        id integer PRIMARY KEY,
        user_id integer);"""
    
        if self.conn is not None:
            self.create_table(notify_table)
            self.create_table(photos_table)
            self.create_table(stream_table)
        
    def create_table(self, cmd):
        try:
            c = self.conn.cursor()
            c.execute(cmd)
        except Error as e:
            print(e)

    def unassign_notify(self, id):
        cmd = ''' DELETE FROM notifications WHERE user_id = ?'''

        cur = self.conn.cursor()
        cur.execute(cmd, (id,))
        self.conn.commit()

    def unassign_photos(self, id):
        cmd = ''' DELETE FROM photos WHERE user_id = ?'''

        cur = self.conn.cursor()
        cur.execute(cmd, (id,))
        self.conn.commit()

    def unassign_streams(self, id):
        cmd = ''' DELETE FROM streaming WHERE user_id = ?'''

        cur = self.conn.cursor()
        cur.execute(cmd, (id,))
        self.conn.commit()

    def fetch_notify_data(self):
        uids = []
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM notifications")
        entries = cur.fetchall()
        for entry in entries:
            uids.append(entry[1])
        return uids
    
    def fetch_photos_data(self):
        uids = []
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM photos")
        entries = cur.fetchall()
        for entry in entries:
            uids.append(entry[1])
        return uids
    
    def fetch_streams_data(self):
        uids = []
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM streaming")
        entries = cur.fetchall()
        for entry in entries:
            uids.append(entry[1])
        return uids

    def add_to_notify(self, id):
        cmd = ''' INSERT INTO notifications(user_id) VALUES(?) '''
        cur = self.conn.cursor()

        cur.execute('SELECT * FROM notifications WHERE (user_id=?)', (id,))
        entry = cur.fetchone()
        if entry is None:
            cur.execute(cmd, (id,))
            self.conn.commit()

        return cur.lastrowid

    def add_to_photos(self, id):
        cmd = ''' INSERT INTO photos(user_id) VALUES(?) '''
        cur = self.conn.cursor()

        cur.execute('SELECT * FROM photos WHERE (user_id=?)', (id,))
        entry = cur.fetchone()
        if entry is None:
            cur.execute(cmd, (id,))
            self.conn.commit()

        return cur.lastrowid

    def add_to_streams(self, id):
        cmd = ''' INSERT INTO streaming(user_id) VALUES(?) '''
        cur = self.conn.cursor()

        cur.execute('SELECT * FROM streaming WHERE (user_id=?)', (id,))
        entry = cur.fetchone()
        if entry is None:
            cur.execute(cmd, (id,))
            self.conn.commit()

        return cur.lastrowid

    def delete_all_notify(self):
        cmd = 'DELETE FROM notifications'
        cur = self.conn.cursor()
        cur.execute(cmd)
        self.conn.commit()

    def delete_all_photos(self):
        cmd = 'DELETE FROM photos'
        cur = self.conn.cursor()
        cur.execute(cmd)
        self.conn.commit()

    def delete_all_streams(self):
        cmd = 'DELETE FROM streaming'
        cur = self.conn.cursor()
        cur.execute(cmd)
        self.conn.commit()

if __name__ == '__main__':
    db = Birdy_DB()
    db.add_to_notify(42)
    db.add_to_notify(55)
    db.add_to_notify(101)
    db.add_to_photos(32)
    db.add_to_photos(7)
    db.add_to_streams(333)
    list = db.fetch_notify_data()
    print(list)
    list = db.fetch_photos_data()
    print(list)
    list = db.fetch_streams_data()
    print(list)
