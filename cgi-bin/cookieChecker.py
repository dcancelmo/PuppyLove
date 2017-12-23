#!/usr/bin/env python
#!C:/Python27/python.exe

import cgitb
import sqlite3
import Cookie
import os
import datetime


cgitb.enable()

conn = sqlite3.connect('createUser.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username varchar(30) primary key, password char(64), timeCreated varchar(26))')

stored_login_cookie = os.environ.get('HTTP_COOKIE')
if stored_login_cookie:
    cookie = Cookie.SimpleCookie(stored_login_cookie)
    rows = c.execute('SELECT * FROM users WHERE username = ?', [cookie['LOGIN'].value])
    rows = rows.fetchone()

    if rows is not None and cookie['LOGIN'] is not None:
        if rows[0] == cookie['LOGIN'].value:
            # Resets expires to be 30 days from last login
            new_cookie = Cookie.SimpleCookie()
            new_cookie['LOGIN'] = cookie['LOGIN'].value
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
            new_cookie['LOGIN']['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S')
            print "Content-Type: text/html"
            print new_cookie
            print "Location: ../dashboard.php"
            print
            # print open('../dashboard.php').read()
        else:
            print "Content-Type: text/html"
            print "Location: ../loginMessages/errorMsg.html"
            print
    else:
        print "Content-Type: text/html"
        print "Location: ../login.html"
        print
else:
    print "Content-Type: text/html"
    print "Location: ../login.html"
    print

conn.commit()
conn.close()
