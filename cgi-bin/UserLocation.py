#!/usr/bin/env python
#!C:/Python27/python.exe

from math import sin, cos, sqrt, atan2, radians


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



def updateUserLocation():
	print
	parameters = cgi.FieldStorage()
	userName = cookie['LOGIN'].value
	longitude = parameters.getvalue("longitude")
	latitude = parameters.getvalue("latitude")
	radius = parameters.getvalue("radius")

	c.execute('CREATE TABLE IF NOT EXISTS userlocation(userName varchar(30) primary key, longitude Decimal(9,7), latitude Decimal(9,7), radius INT)')
	c.execute('UPDATE profiles SET longitude=?, latitude=?, radius=? WHERE userName=?',[longitude, latitude, radius, userName])
	
	
	try:
		response = " tried "
		c.execute('INSERT INTO userlocation(userName, longitude, latitude, radius) VALUES(?, ?, ?,?)',[userName, longitude, latitude, radius])
		
	except sqlite3.Error as er:
		response = " excepted "
		c.execute('UPDATE userlocation SET longitude=?, latitude=?, radius=? WHERE userName=?',[longitude, latitude, radius, userName])
	
	
	
	coord = [{'lng' : longitude, 'lat' : latitude}]

	conn.commit()
	conn.close()
	return json.dumps({'response': longitude})



updateUserLocation()


