#!C:\Python27\python.exe

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
conn = sqlite3.connect(database_name)
c = conn.cursor

form = cgi.FieldStorage()
userName = "Need to get this information somehow"
humanName = str(form['username'].value)
dogName = str(form['dogName'].value)
description = str(form['description'].value)
genderPref = str(form['gender'].value)

c.execute('CREATE TABLE IF NOT EXISTS profiles(username varchar(30) primary key, humanName varchar(30), dogName varchar(30), description varchar(200), genderPref varchar(6)')

c.execute('INSERT INTO profiles(userName, humanName, dogName, description, genderPref) VALUES(?, ?, ? , ?, ?)', [userName, humanName, dogName, description, genderPref])

print '''
    <html>
        <head>
            <title>Profile Updated</title>
        </head>
        <body>
            <h1>Successfully updated profile!</h1>
            <h2>'''
print "Username: " + userName
print "Name: " + humanName
print "Your dog's name: " + dogName
print "Description: " + description
print "Gender Preference: " + genderPref
print'''</h2>
        </body>
    </html>
'''

conn.commit()
conn.close()
