#!/usr/bin/env python

import cgitb
import cgi
import sqlite3
import Cookie
import os
import datetime
from hashlib import sha256

cgitb.enable()

conn = sqlite3.connect('createUser.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username varchar(30) primary key, password char(64), timeCreated varchar(26))')

stored_login_cookie = os.environ.get('HTTP_COOKIE')
if stored_login_cookie:
    cookie = Cookie.SimpleCookie(stored_login_cookie)
    rows = c.execute('SELECT * FROM users WHERE username = ?', [cookie['LOGIN'].value])
    rows = rows.fetchone()

    if rows[0] == cookie['LOGIN'].value:
        # Resets expires to be 30 days from last login
        new_cookie = Cookie.SimpleCookie()
        new_cookie['LOGIN'] = cookie['LOGIN'].value
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        new_cookie['LOGIN']['expires'] = expires.strftime("%a,%d%b%Y%H:%M:%SGMT")
        print "Content-Type: text/html"
        print new_cookie
        print
        print '''<html>
                    <head>
                    <title>Correct Login</title>
                    </head>
                    <body>
                    <p>You logged in automatically with a cookie!</p>
                    <p>'''
        print 'Your name: ' + new_cookie['LOGIN'].value
        print '''</p>
                    </body>
                    </html>
                    '''
    else:
        print 'Content-Type: text/html'
        print
        print '''<html>
                <head>
                    <title>Error</title>
                </head>
                <body>
                    <p>An error has occurred.</p>
                    <p><a href="localhost">Go back</a></p>
                </body>
                </html>
                '''
else:
    form = cgi.FieldStorage()

    userName = form['username'].value
    password = form['password'].value

    rows = c.execute('SELECT * FROM users WHERE username = ?', [userName])
    rows = rows.fetchone()

    hashed_pass = rows[1]
    salt = rows[2]
    test_pass = password + salt
    test_pass = sha256(test_pass.encode('ascii')).hexdigest()
    if hashed_pass == test_pass:
        print 'Content-Type: text/html'
        if not stored_login_cookie:
            cookie = Cookie.SimpleCookie()
            cookie['LOGIN'] = userName
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
            cookie['LOGIN']['expires'] = expires.strftime("%a,%d%b%Y%H:%M:%SGMT")
            print cookie
        print
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
