#!/usr/bin/env python

import cgitb
import cgi
import sqlite3
import Cookie
import os
import datetime

cgitb.enable()

new_cookie = Cookie.SimpleCookie()
new_cookie['LOGIN'].value = 0;
expires = datetime.datetime.utcnow() - datetime.timedelta(days=100)
new_cookie['LOGIN']['expires'] = expire.strftime("%a,%d%b%Y%H:%M:%SGMT")

print "Content-Type: text/html"
print
print '''<!doctype html>
<html>
<head>
<title>Logout</title>
<head>
<body>
<p>You have been logged out</p>
</body>
</html>'''