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

def getPotentialMatches():
	parameters = cgi.FieldStorage()
	c_genderPref = parameters.getvalue("genderPref")
	c_gender = parameters.getvalue("gender")
	c_userName = parameters.getvalue("userName")
	#print "Content-Type: application/json"
	print
    #print cookie['LOGIN'].value
	#get the users full name
	username = cookie['LOGIN'].value
	#print username
	select_stmt = ''
	select_stmt_both = "SELECT * FROM profiles WHERE (genderPref='{}' OR genderPref='{}') AND userName !='{}'".format(c_gender, 'both', c_userName)
	if c_genderPref == 'both':
		select_stmt = select_stmt_both;
	else:
		select_stmt = "SELECT * FROM profiles WHERE gender='{}' AND (genderPref='{}' OR genderPref='{}') AND userName!='{}'".format(c_genderPref, c_gender, 'both', c_userName)
	user_rows = c.execute(select_stmt).fetchall()
	# user_rows = c.execute('SELECT * FROM profiles WHERE gender=? AND (genderPref=? OR genderPref=?)',
	#  ['female', 'male', 'both'])
	data = []
	if user_rows is not None:
		
		
		for row in user_rows:
			entry = {
				'username': row[0],
				'userPic' : row[1].encode('base64'),
				'humanName' : row[2],
				'dogPic' : row[3].encode('base64'),
				'dogName' : row[4],
				'description' :row[5],
				'genderPref' :row[6],
				'gender' :row[7]
			}
			#data.append(row)
			data.append(entry)
			
			
		with open('test.txt', 'w') as outfile:
			json.dump(data, outfile)
		print json.dumps(data)
getPotentialMatches()

