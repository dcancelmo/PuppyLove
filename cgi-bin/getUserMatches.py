#!/usr/bin/env python
import math
from math import sin, cos, sqrt, atan2, radians
import cgitb
import os
import cgi
import sqlite3
import Cookie
import json
import struct #need this to convert coords to floats not doubles
cgitb.enable()

conn = sqlite3.connect('createUser.db')
conn.text_factory = str #need to change the text_factory for the images
c = conn.cursor()

stored_login_cookie = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie(stored_login_cookie)

# There is probably a much better way to do this


def getMatches():
	print
	parameters = cgi.FieldStorage()
	username = cookie['LOGIN'].value
	match_rows = c.execute("SELECT * FROM matches WHERE user1=?", [username])
	matches = match_rows.fetchall()#only when curruser = user1 
	data = []
	if matches is not None:
		for match in matches:
			user2_select = c.execute("SELECT * FROM profiles WHERE userName=?", [match[1]])
			user_row = user2_select.fetchone()
			if user_row is not None:
				entry = {
					'username': user_row[0],
					'userPic' : user_row[1].encode('base64'),
					'humanName' : user_row[2],
					'dogPic' : user_row[3].encode('base64'),
					'dogName' : user_row[4],
					'description' :user_row[5],
					'phoneNumber' : user_row[11]
				}
				data.append(entry)
	match_rows = c.execute("SELECT * FROM matches WHERE user2=?", [username])
	matches = match_rows.fetchall()#only when curruser = user2
	
	if matches is not None:
		for match in matches:
			user1_select = c.execute("SELECT * FROM profiles WHERE userName=?", [match[0]])
			user_row = user1_select.fetchone()
			if user_row is not None:
				entry = {
					'username': user_row[0],
					'userPic' : user_row[1].encode('base64'),
					'humanName' : user_row[2],
					'dogPic' : user_row[3].encode('base64'),
					'dogName' : user_row[4],
					'description' :user_row[5],
					'phoneNumber' : user_row[11]
				}
				data.append(entry)
			
	with open('test.txt', 'w') as outfile:
		json.dump(data, outfile)
	print json.dumps(data)

getMatches()

