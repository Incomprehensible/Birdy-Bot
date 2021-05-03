import sqlite3
from sqlite3 import Error

def delete_all_notify(conn):
    cmd = 'DELETE FROM notifications'
    cur = conn.cursor()
    cur.execute(cmd)
    conn.commit()

def delete_all_photos(conn):
    cmd = 'DELETE FROM photos'
    cur = conn.cursor()
    cur.execute(cmd)
    conn.commit()

def delete_all_streams(conn):
    cmd = 'DELETE FROM streaming'
    cur = conn.cursor()
    cur.execute(cmd)
    conn.commit()

def unassign_notify(conn, id):
    cmd = ''' DELETE FROM notifications WHERE user_id = ?'''

    cur = conn.cursor()
    cur.execute(cmd, (id,))
    conn.commit()

def unassign_photos(conn, id):
    cmd = ''' DELETE FROM photos WHERE user_id = ?'''

    cur = conn.cursor()
    cur.execute(cmd, (id,))
    conn.commit()

def unassign_streams(conn, id):
    cmd = ''' DELETE FROM streaming WHERE user_id = ?'''

    cur = conn.cursor()
    cur.execute(cmd, (id,))
    conn.commit()

def add_to_notify(conn, id):
    cmd = ''' INSERT INTO notifications(user_id) VALUES(?) '''
    cur = conn.cursor()

    cur.execute('SELECT * FROM notifications WHERE (user_id=?)', (id,))
    entry = cur.fetchone()
    if entry is None:
        cur.execute(cmd, (id,))
        conn.commit()

    return cur.lastrowid

def add_to_photos(conn, id):
    cmd = ''' INSERT INTO photos(user_id) VALUES(?) '''
    cur = conn.cursor()

    cur.execute('SELECT * FROM photos WHERE (user_id=?)', (id,))
    entry = cur.fetchone()
    if entry is None:
        cur.execute(cmd, (id,))
        conn.commit()

    return cur.lastrowid

def add_to_streams(conn, id):
    cmd = ''' INSERT INTO streaming(user_id) VALUES(?) '''
    cur = conn.cursor()

    cur.execute('SELECT * FROM streaming WHERE (user_id=?)', (id,))
    entry = cur.fetchone()
    if entry is None:
        cur.execute(cmd, (id,))
        conn.commit()

    return cur.lastrowid

def create_table(conn, cmd):
    try:
        c = conn.cursor()
        c.execute(cmd)
    except Error as e:
        print(e)

def create_connection(db_file=r"db/birdy.db"):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    
    return conn

if __name__ == '__main__':
    conn = create_connection(r"db/birdy.db")
    notify_table = """ CREATE TABLE IF NOT EXISTS notifications (
        id integer PRIMARY KEY,
        user_id integer); """

    photos_table = """CREATE TABLE IF NOT EXISTS photos (
        id integer PRIMARY KEY,
        user_id integer);"""
    
    stream_table = """CREATE TABLE IF NOT EXISTS streaming (
        id integer PRIMARY KEY,
        user_id integer);"""
    
    if conn is not None:
        create_table(conn, notify_table)
        create_table(conn, photos_table)
        create_table(conn, stream_table)
    
    with conn:
        cmd = (32)
        add_to_notify(conn, cmd)
        add_to_photos(conn, cmd)
        add_to_streams(conn, cmd)
        cmd = (300)
        add_to_notify(conn, cmd)
        add_to_photos(conn, cmd)
        add_to_streams(conn, cmd)
        cmd = (5)
        add_to_notify(conn, cmd)
        add_to_photos(conn, cmd)
        add_to_streams(conn, cmd)
        cmd = (8)
        add_to_notify(conn, cmd)
        add_to_photos(conn, cmd)
        add_to_streams(conn, cmd)
        cmd = (8)
        unassign_notify(conn, cmd)
        unassign_photos(conn, cmd)
        unassign_streams(conn, cmd)
        # delete_all_streams(conn)
        # delete_all_photos(conn)
        # delete_all_notify(conn)
