#!/usr/bin/env python
#!C:/Python27/python.exe

import Cookie
import cgitb
import sqlite3

import os

import getLoginCookie
import cgi


cgitb.enable()

conn = sqlite3.connect('createUser.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username varchar(30) primary key, password char(64), timeCreated varchar(26))')

stored_login_cookie = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie(stored_login_cookie)

username = cookie['LOGIN'].value


c.execute('DELETE FROM users WHERE username=?', [username])
c.execute('DELETE FROM profiles WHERE userName=?', [username])

# c.execute('DELETE FROM likes WHERE liker=?', [username])
# c.execute('DELETE  FROM likes WHERE likee=?', [username])
# c.execute('DELETE FROM matches WHERE p1=?', [username])
# c.execute('DELETE FROM matches WHERE p2=?', [username])

conn.commit()
conn.close()
