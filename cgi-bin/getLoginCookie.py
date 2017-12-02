#!/usr/bin/env python
#!C:/Python27/python.exe

import cgitb
import os
import cgi
import sqlite3
import Cookie

cgitb.enable()

conn = sqlite3.connect('createUser.db')
c = conn.cursor()

stored_login_cookie = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie(stored_login_cookie)

# There is probably a much better way to do this
def getCookie():
    print "Content-Type: text/html"
    print
    print cookie['LOGIN'].value

getCookie()
