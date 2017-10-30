#!/usr/bin/env python

import cgitb
import sqlite3
import cgi
from PIL import Image

cgitb.enable()

print 'Content-Type: text/html'
print

database_name = 'createUser.db'
table_name = 'profiles'

form = cgi.FieldStorage()

humanName = str(form['username'].value)
profPic = form['userPic']
dogName = str(form['dogName'].value)
