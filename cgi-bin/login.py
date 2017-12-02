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
    #rows = rows.fetchone()
    if rows.rowcount > 0: #unused code block?
        # Resets expires to be 30 days from last login
        new_cookie = Cookie.SimpleCookie()
        new_cookie['LOGIN'] = cookie['LOGIN'].value
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        new_cookie['LOGIN']['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S')
        print "Content-Type: text/html"
        print new_cookie.output()
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
        form = cgi.FieldStorage()
        if ('username' in form) & ('password' in form):
            userName = form['username'].value
            password = form['password'].value
            rows = c.execute('SELECT * FROM users WHERE username = ?', [userName])
            rows = rows.fetchone()
            if rows is not None:
                hashed_pass = rows[1]
                salt = rows[2]
                test_pass = password + salt
                test_pass = sha256(test_pass.encode('ascii')).hexdigest()

                if hashed_pass == test_pass:
                    print 'Content-Type: text/html'
                    cookie = Cookie.SimpleCookie()
                    cookie['LOGIN'] = userName
                    expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
                    cookie['LOGIN']['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S')
                    print cookie.output()
                    print
                    # print '''<html>
                    #         <head>
                    #             <title>Correct Login</title>
                    #         </head>
                    #         <body>
                    #         <p>You are logged in</p>
                    #         <p>'''
                    # print "Your name: " + userName
                    # print '''</p>
                    #             <form method="post" action="/cgi-bin/logout.py"><br><br>
                    #                 <button type="submit" class="btn-default" name="logout"> Logout </button>
                    #             </form>
                    #         </body>
                    #         </html>
                    #         '''
                    #print "Content-Type: text/html"
                    print open('../user_profile.html').read()
                else:
                    print "Content-Type: text/html"
                    print "Location: ../loginMessages/incorrect.html"
                    print
            else:
                print "Content-Type: text/html"
                print "Location: ../loginMessages/incorrect.html"
                print
        else:
            print 'Content-Type: text/html'
            print "Location: ../loginMessages/missingInfo.html"
            print
else:
    form = cgi.FieldStorage()
    if ('username' in form) & ('password' in form):
        userName = form['username'].value
        password = form['password'].value
        rowsCur = c.execute('SELECT * FROM users WHERE username = ?', [userName])
        rows = rowsCur.fetchone()
        if rows is not None:
            hashed_pass = rows[1]
            salt = rows[2]
            test_pass = password + salt
            test_pass = sha256(test_pass.encode('ascii')).hexdigest()
            if hashed_pass == test_pass:
                print 'Content-Type: text/html'
                cookie = Cookie.SimpleCookie()
                cookie['LOGIN'] = userName
                expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
                cookie['LOGIN']['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S')
                print cookie.output()
                print
                # print '''<html>
                #     <head>
                #         <title>Correct Login</title>
                #     </head>
                #     <body>
                #     <p>You are logged in</p>
                #     <p>'''
                # print "Your name: " + userName
                # print '''</p>
                #     </body>
                #     </html>
                #     '''
                print open('../user_profile.html').read()
            else:
                print "Content-Type: text/html"
                print "Location: ../loginMessages/incorrect.html"
                print
        else:
            print 'Content-Type: text/html'
            print "Location: ../loginMessages/errorMsg.html"
            print
    else:
        #It shouldn't ever reach here, but just in case
        print "Content-Type: text/html"
        print "Location: ../loginMessages/missingInfo.html"
        print

conn.commit()
conn.close()