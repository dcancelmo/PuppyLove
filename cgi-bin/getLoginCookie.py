#!/usr/bin/env python

import cgitb
import os
import cgi
import sqlite3
import Cookie

cgitb.enable()

conn = sqlite3.connect('createUser.db')
c = conn.cursor()

# There is probably a much better way to do this
stored_login_cookie = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie(stored_login_cookie)
print "Content-Type: text/html"
print
print cookie['LOGIN'].value
