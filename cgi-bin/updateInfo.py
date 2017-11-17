#!/usr/bin/env python

import cgitb
import sqlite3
import Cookie
import cgi
import os

cgitb.enable()
#how to display BLOB image:
#print '<img  src=\"data:;base64,'+humanPic.encode('base64')+'\"/>'
#where humanPic is the original input from uploading the image

print 'Content-Type: text/html'

#Get form information
form = cgi.FieldStorage()

#Update database
database_name = 'createUser.db'
conn = sqlite3.connect(database_name)
conn.text_factory = str
c = conn.cursor()


def getCookieValue():
    stored_login_cookie = os.environ.get('HTTP_COOKIE')
    cookie = Cookie.SimpleCookie(stored_login_cookie)
    return cookie['LOGIN'].value


userName = getCookieValue()
#c.execute('DROP TABLE IF EXISTS profiles')
c.execute('CREATE TABLE IF NOT EXISTS profiles(userName varchar(30) primary key, userPic BLOB, humanName varchar(30), dogPic BLOB,  dogName varchar(30), description varchar(200), genderPref varchar(10))')

# if 'humanName' in form:
#     humanName = str(form['username'].value)
# if 'dogName' in form:
#     dogName = str(form['dogName'].value)
# if 'description' in form:
#     description = str(form['description'].value)
# if 'genderPref' in form:
#     genderPref = str(form['gender'].value)

humanName = str(form['username'].value)
humanPic = str(form['userPic'].value)

dogPic = str(form['dogPic'].value)
dogName = str(form['dogName'].value)

description = str(form['description'].value)
genderPref = str(form['gender'].value)

try:
    print
    c.execute('INSERT INTO profiles(userName, userPic, humanName, dogPic,  dogName, description, genderPref) VALUES(?, ?, ?, ?, ?, ?, ?)', [userName, humanPic, humanName, dogPic, dogName, description, genderPref])

    print '''<html>
        <head>
            <title>Profile Updated</title>
        </head>
        <body>
            <h1>Successfully updated profile!</h1>
            <h2>'''
    print "Username: " + userName
    print "Name: " + humanName
    print "userPic: " + humanPic.encode('base64')
    print '<img  src=\"data:;base64,'+humanPic.encode('base64')+'\"/>'
    print "Your dog's name: " + dogName
    print "Description: " + description
    print "Gender Preference: " + genderPref
    print'''</h2>
        </body>
    </html>
    '''
except sqlite3.Error as er:
    c.execute('UPDATE profiles SET humanName=? , userPic=?, dogPic=?, dogName=? , description=? , genderPref=? WHERE userName=?', (humanName, humanPic, dogPic, dogName, description, genderPref, userName))
    
    print
    print '''<html>
        <head>
            <title>Profile Updated</title>
        </head>
        <body>
            <h1>Successfully updated profile!</h1>
            <h2>'''
    print "Username: " + userName
    print "Name: " + humanName
    print "UserPic: " + humanPic.decode('base64')
    print '<img  src=\"data:;base64,'+humanPic.encode('base64')+'\"/>'
    print "Your dog's name: " + dogName
    print "Description: " + description
    print "Gender Preference: " + genderPref
    print'</h2>'
    print '''
        </body>
    </html>
    '''

conn.commit()
conn.close()
