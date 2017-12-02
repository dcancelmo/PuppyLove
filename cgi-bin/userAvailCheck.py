#!/usr/bin/env python

import cgitb
import sqlite3


cgitb.enable()

conn = sqlite3.connect('createUser.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username varchar(30) primary key, password char(64), timeCreated varchar(26))')


def checkAvail(userP):
    rows = c.execute('SELECT username from users WHERE username=?', [userP])
    if rows is None:
        return True
    else:
        return False

