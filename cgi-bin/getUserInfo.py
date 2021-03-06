#!/usr/bin/env python
#!C:/Python27/python.exe

import cgitb
import os
import cgi
import sqlite3
import Cookie
import json

cgitb.enable()

conn = sqlite3.connect('createUser.db')
conn.text_factory = str #need to change the text_factory for the images
c = conn.cursor()

stored_login_cookie = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie(stored_login_cookie)

# There is probably a much better way to do this

def getUserProfileInfo():
	# print "Content-Type: application/json"
	print
	# get the users full name
	username = cookie['LOGIN'].value
	# print username
	user_rows = c.execute('SELECT * FROM profiles WHERE userName=?', [username]) #should return only one
	user_rows = c.fetchone()
	if user_rows is None:
		response = user_rows

	if user_rows is not None:
		response = {'userName': user_rows[0],'gender': user_rows[7],'genderPref': user_rows[6],
		'description': user_rows[5],'humanName': user_rows[2], 'dogName': user_rows[4], 
		'dogPic' : user_rows[3].encode('base64'), 'humanPic': user_rows[1].encode('base64'),
		'longitude' : user_rows[8], 'latitude' : user_rows[9], 'radius' : user_rows[10], 'phoneNumber' : user_rows[11]}

		print json.dumps(response)




getUserProfileInfo()

