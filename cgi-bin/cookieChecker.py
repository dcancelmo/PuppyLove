#!/usr/bin/env python

import cgitb
import sqlite3
import Cookie
import os
import datetime


cgitb.enable()

conn = sqlite3.connect('createUser.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username varchar(30) primary key, password char(64), timeCreated varchar(26))')

stored_login_cookie = os.environ.get('HTTP_COOKIE')
if stored_login_cookie:
    cookie = Cookie.SimpleCookie(stored_login_cookie)
    rows = c.execute('SELECT * FROM users WHERE username = ?', [cookie['LOGIN'].value])
    rows = rows.fetchone()

    # print "Content-Type: text/html"
    # print
    # print '''<html>
    #                 <head>
    #                     <title>Error</title>
    #                 </head>
    #                 <body>
    #                     <p>An error has occurred.</p>'''
    # print 'Your name: ' + cookie['LOGIN'].value
    # print '''<p><a href="../login.html">Go back</a></p>
    #                 </body>
    #                 </html>
    #                 '''
    if rows is not None:
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
                            <form method="post" action="/cgi-bin/logout.py"><br><br>
                            <button type="submit" class="btn-default" name="logout"> Logout </button>
                        </body>
                        </html>
                        '''
        else:
            # print "Content-Type: text/html"
            # print "Location: http://localhost/login.html"
            # print
            print "Content-Type: text/html"
            print
            print '''<html>
                    <head>
                        <title>Error</title>
                    </head>
                    <body>
                        <p>An error has occurred.</p>
                        <p><a href="../login.html">Go back</a></p>
                    </body>
                    </html>
                    '''
    else:
        print "Content-Type: text/html"
        print "Location: http://localhost/login.html"
        print
else:
    print "Content-Type: text/html"
    print
    print'''<html>
    <head>
        <title>Puppy Love </title>
        <meta charset="UTF-8">
        <style>
        body {
            text-align: center;
            font-family: sans-serif;
        }
        </style>
    </head>
    <body>
        <div id="title">
            <h1>Login</h1>
        </div>
        <br>
        <form method = "post" action="/cgi-bin/login.py">
            Username: <input type="text" name="username">
            <br>
            Password: <input type="password" name="password">
            <br>
            <button type="submit"> Login </button>
        </form>
        <h4><a href="/account-create.html">Or create a new account!</a></h4>
    </body>
</html>'''

conn.commit()
conn.close()
