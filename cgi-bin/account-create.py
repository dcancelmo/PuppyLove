#!/usr/bin/env python

import cgitb
import sqlite3
import cgi
import datetime
from hashlib import sha256

cgitb.enable()

print 'Content-Type: text/html'
print

database_name = 'createUser.db'
table_name = 'users'

form = cgi.FieldStorage()
username = str(form['username'].value)
password = str(form['password'].value)
passwordConfirm = str(form['passwordConfirm'].value)
if (password != passwordConfirm):
    print '''<html>
            <head>
                <title>Invalid</title>
            </head>
            <body>
                <h1>Passwords do not match</h1>
                <h2>
            </body>
        </html>
        '''
else:
    timestamp = str(datetime.datetime.now())
    password = password + timestamp
    hashPass = sha256(password.encode('ascii')).hexdigest()

    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS users(username varchar(30) primary key, password char(64), timeCreated varchar(26))')

    #Check if already in database
    #queryName = c.execute('SELECT username FROM ' + table_name + ' WHERE username=?', [username]).fetchone()
    #if queryName is not username:
    try:
        c.execute('INSERT INTO users (username, password, timeCreated) VALUES (?, ?, ?)', [username, hashPass, timestamp])
        print '''<html>
            <head>
                <title>Success</title>
            </head>
            <body>
                <h1>Successful account creation</h1>
                <h2>'''
        print "Username: " + username
        print "<br/>Time created: " + timestamp
        print '''</h2>
            </body>
        </html>
        '''
    #else:
    except sqlite3.IntegrityError:
        print '''<html>
                <head>
                    <title>Invalid</title>
                </head>
                <body>
                    <h3>Username unavailable</h3>
                </body>
            </html>
            '''

    conn.commit()
    conn.close()
