#!/usr/bin/env python
#!C:/Python27/python.exe

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

def calculateDistance(coordA, coordB, radiusA, radiusB):

	earths_radius = 3963.1676 #in miles
	

	lat1 = radians(float(coordA['lat']))
	lon1 = radians(float(coordA['lng']))
	
	lat2 = radians(float(coordB['lat']))
	lon2 = radians(float(coordB['lng']))

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = earths_radius * c

	
	return {'boolean' :(distance <= radiusA) & (distance <= radiusB), 'distance' : distance}

def getPotentialMatches():
	parameters = cgi.FieldStorage()
	c_genderPref = parameters.getvalue("genderPref")
	c_gender = parameters.getvalue("gender")
	c_userName = parameters.getvalue("userName")
	lng = parameters.getvalue("longitude")
	lat = parameters.getvalue("latitude")
	coordA = {'lng':lng, 'lat':lat}
	radiusA = parameters.getvalue("radius")

	print
	# get the users full name
	username = cookie['LOGIN'].value
	select_stmt = ''
	select_stmt_both = "SELECT * FROM profiles WHERE (genderPref='{}' OR genderPref='{}') AND userName !='{}'".format(c_gender, 'both', c_userName)
	if c_genderPref == 'both':
		select_stmt = select_stmt_both;
	else:
		select_stmt = "SELECT * FROM profiles WHERE gender='{}' AND (genderPref='{}' OR genderPref='{}') AND userName!='{}'".format(c_genderPref, c_gender, 'both', c_userName)
	user_rows = c.execute(select_stmt).fetchall()
	data = []
	if user_rows is not None:
		
		for row in user_rows: 
			radiusB = row[10]
			lngB = row[8]
			latB = row[9]
			coordB = {'lng':lngB, 'lat':latB}
			bool_returned = calculateDistance(coordA, coordB, radiusA, radiusB)['boolean']
			distance = calculateDistance(coordA, coordB, radiusA, radiusB)['distance']
			if bool_returned: # if within radius preference
				# check if never liked/passed this person before
				c.execute('CREATE TABLE IF NOT EXISTS likes(liker VARCHAR(30), likee VARCHAR(30), like_or_hate VARCHAR(30))')
				seen_check = c.execute("SELECT * FROM likes WHERE liker=? AND likee=?",[username, row[0]])
				if seen_check.fetchone() is None: #if they have not seen this person bfore
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
						'radius' :row[10],
						'distance' : distance
					}
					data.append(entry)
			
			
		# with open('test.txt', 'w') as outfile:
		# 	json.dump(data, outfile)
		print
		print json.dumps(data)
getPotentialMatches()
