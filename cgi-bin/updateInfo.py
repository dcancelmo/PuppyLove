#!/usr/bin/env python
# coding=utf-8

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
conn.text_factory = str #need to change the text_factory for the images
c = conn.cursor()


def getCookieValue():
    stored_login_cookie = os.environ.get('HTTP_COOKIE')
    cookie = Cookie.SimpleCookie(stored_login_cookie)
    return cookie['LOGIN'].value


userName = getCookieValue()
c.execute('CREATE TABLE IF NOT EXISTS profiles(userName varchar(30) primary key, userPic BLOB, humanName varchar(30), dogPic BLOB,  dogName varchar(30), description varchar(200), genderPref varchar(10), gender varchar(10), longitude Decimal(9,7), latitude Decimal(9,7), radius int, phoneNumber varchar(30))')


humanName = str(form['username'].value)
humanPic = str(form['userPic'].value)
dogPic = str(form['dogPic'].value)
dogName = str(form['dogName'].value)

description = str(form['description'].value)
gender = str(form['gender'].value)
genderPref = str(form['genderPref'].value)
newUser = str(form['newUser'].value)
longitude = str(form['longitude'].value)
latitude = str(form['latitude'].value)
radius = str(form['radius'].value)
phoneNumber = str(form['phoneNumber'].value)


try:
    c.execute('INSERT INTO profiles(userName, userPic, humanName, dogPic,  dogName, description, genderPref, gender, longitude, latitude, radius, phoneNumber) VALUES(?,?, ?, ?, ? , ?, ?, ?,?,?,?,?)', [userName, humanPic, humanName, dogPic, dogName, description, genderPref, gender, longitude, latitude, radius, phoneNumber])
    print "Location: ../view_profile.php"
    print

except sqlite3.Error as er:

    if humanPic is "" and dogPic is "":
        c.execute('UPDATE profiles SET humanName=?, dogName=? , description=? , genderPref=?, gender=?,longitude=?, latitude=?,radius=?, phoneNumber=?  WHERE userName=?',[humanName, dogName, description, genderPref, gender,longitude,latitude,radius, phoneNumber,  userName])
    elif dogPic is "":
        c.execute('UPDATE profiles SET humanName=? , userPic=?, dogName=? , description=? , genderPref=?, gender=?,longitude=?, latitude=?,radius=?, phoneNumber=?  WHERE userName=?',[humanName, humanPic, dogName, description, genderPref, gender,longitude,latitude, radius, phoneNumber, userName])
    elif humanPic is "":
        c.execute('UPDATE profiles SET humanName=?, dogPic=?, dogName=? , description=? , genderPref=?, gender=? ,longitude=?, latitude=?,radius=?, phoneNumber=? WHERE userName=?',[humanName, dogPic, dogName, description, genderPref, gender, longitude,latitude, radius, phoneNumber, userName])
    else:
        c.execute('UPDATE profiles SET humanName=? , userPic=?, dogPic=?, dogName=? , description=? , genderPref=?, gender=? ,longitude=?, latitude=?,radius=?, phoneNumber=? WHERE userName=?',[humanName, humanPic, dogPic, dogName, description, genderPref, gender, longitude,latitude,radius, phoneNumber, userName])

    print "Location: ../view_profile.php"
    print


conn.commit()
conn.close()
