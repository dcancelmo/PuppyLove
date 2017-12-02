#!/usr/bin/env python

import cgitb
import sqlite3
import Cookie
import cgi
import os
from PIL import Image

cgitb.enable()

print 'Content-Type: text/html'
print

database_name = 'createUser.db'
table_name = 'profiles'
conn = sqlite3.connect(database_name)
c = conn.cursor()

form = cgi.FieldStorage()

stored_login_cookie = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie(stored_login_cookie)
rows = c.execute('SELECT * FROM users WHERE username = ?', [cookie['LOGIN'].value])
rows = rows.fetchone()

humanName = str(form['username'].value)
profPic = form['userPic']
dogName = str(form['dogName'].value)

conn.commit()
conn.close()