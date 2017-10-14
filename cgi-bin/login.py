#!/usr/bin/env python

import cgitb
import cgi
import sqlite3
from hashlib import sha256

cgitb.enable()

print 'Content-Type: text/html'
print

form = cgi.FieldStorage()

userName = form['username'].value
password = form['password'].value

conn = sqlite3.connect('createUser.db')
c = conn.cursor()
    
c.execute('CREATE TABLE IF NOT EXISTS users(username varchar(30) primary key, password char(64), timeCreated varchar(26))')

rows = c.execute('SELECT * FROM users WHERE username = ?', [userName])
rows = rows.fetchone();

hashed_pass = rows[1]
salt = rows[2]
test_pass = password + salt
test_pass = sha256(test_pass.encode('ascii')).hexdigest();
if hashed_pass == test_pass:
    print '''<html>
        <head>
            <title>Correct Login</title>
        </head>
        <body>
        <p>'''
    print "Your name: " + userName

    print "Your Password: " + password
    print '''</p>
        </body>
        </html>
        '''
else:
    print '''<html>
        <head>
            <title>Incorrect Login</title>
        </head>
        <body>
            <p>Incorrect username/password</p>
        </body>
        </html>
        '''

conn.commit()
conn.close()
