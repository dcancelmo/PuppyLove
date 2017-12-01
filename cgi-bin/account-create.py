#!/usr/bin/env python

import cgitb
import sqlite3
import cgi
import datetime
import Cookie
from hashlib import sha256

cgitb.enable()

print 'Content-Type: text/html'

database_name = 'createUser.db'
table_name = 'users'

form = cgi.FieldStorage()
if ('username' in form) & ('password' in form) & ('passwordConfirm' in form):
    # if form is not None:
    username = str(form['username'].value)
    password = str(form['password'].value)
    passwordConfirm = str(form['passwordConfirm'].value)
    if password != passwordConfirm:
        # It shouldn't ever reach here. But...
        print
        print '''<html>
                <head>
                    <title>Invalid</title>
                </head>
                <body>
                    <h1>Passwords do not match</h1>
                    <p><a href="../account-create.html">Go back to account creation</a></p>
                </body>
            </html>
            '''
    else:
        timestamp = str(datetime.datetime.now())
        password = password + timestamp
        hashPass = sha256(password.encode('ascii')).hexdigest()

        conn = sqlite3.connect(database_name)
        c = conn.cursor()

        c.execute(
            'CREATE TABLE IF NOT EXISTS users(username VARCHAR(30) PRIMARY KEY, password char(64), timeCreated VARCHAR(26))')

        # Check if already in database
        # queryName = c.execute('SELECT username FROM ' + table_name + ' WHERE username=?', [username]).fetchone()
        # if queryName is not username:
        try:
            c.execute('INSERT INTO users (username, password, timeCreated) VALUES (?, ?, ?)',
                      [username, hashPass, timestamp])
            cookie = Cookie.SimpleCookie()
            cookie['LOGIN'] = username
            expires = datetime.datetime.now() + datetime.timedelta(days=30)
            cookie['LOGIN']['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S')
            print cookie.output()
            print "Location: /user_profile.html"
            print
            # print '''<html>
            #     <head>
            #         <title>Success</title>
            #     </head>
            #     <body>
            #         <h1>Successful account creation</h1>
            #         <h2>'''
            # print "Username: " + username
            # print "<br/>Time created: " + timestamp
            # print "<br/>" + cookie.output()
            # print '''</h2>
            #         <p><a href="cookieChecker.py">Go to main page</a>
            #     </body>
            # </html>
            # '''
        # else:
        except sqlite3.IntegrityError:
            print
            print '''<html>
                    <head>
                        <title>Invalid</title>
                        <script type = "text/javascript">
                        	sessionStorage.setItem("message", "Username already taken please choose another.");
                        	window.location.href = "../account-create.html";
                        </script>
                    </head>
                    <body>
                    </body>
                </html>
                '''
        conn.commit()
        conn.close()
else:
    # It shouldn't ever reach here. But just in case...
    print
    print '''<html>
                <head>
                    <title>Invalid</title>
                </head>
                <body>
                    <h3>You did not fill every entry.</h3>
                    <p><a href="../account-create.html">Go back to account creation</a></p>
                </body>
            </html>
            '''


