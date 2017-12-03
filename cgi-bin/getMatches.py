#!/usr/bin/env python

import cgitb
import os
import cgi
import sqlite3
import Cookie
import json

cgitb.enable()

conn = sqlite3.connect('createUser.db')
conn.text_factory = str
c = conn.cursor()

stored_login_cookie = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie(stored_login_cookie)

def getMatches():
	username = cookie['LOGIN'].value

	get_matches = "SELECT * FROM matches WHERE p1 = '{}' OR p2 = '{}'".format(username, username)

	user_rows = c.execute(get_matches).fetchall()

	data = []

	if user_rows is not None:
		for row in user_rows:
			if row[0] is username:
				match_profile = row[1]
			else:
				match_profile = row[0]


			get_user_prof = "SELECT * FROM profiles WHERE userName = '{}'".format(match_profile)

			user_prof = c.execute(get_user_prof).fetchall()

			if user_prof is not None:
				for row in user_prof:
					entry = {
						'username': row[0],
						'userPic' : row[1].encode('base64'),
						'humanName' : row[2],
						'dogPic' : row[3].encode('base64'),
						'dogName' : row[4],
						'description' :row[5],
						'genderPref' :row[6],
						'gender' :row[7],
						'longitude' : row[8],
						'latitude' : row[9],
						'radius' :row[10]
					}
					data.append(entry)
		print json.dumps(data)

getMatches()