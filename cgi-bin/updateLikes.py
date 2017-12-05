#!/usr/bin/env python
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



def updateLikes():
	print
	#print "Content-Type: application/json"
	parameters = cgi.FieldStorage()
	userName = cookie['LOGIN'].value
	liker = parameters.getvalue('liker') #username
	liker = userName
	likee = parameters.getvalue('likee')
	like_or_hate = parameters.getvalue('like_or_hate')

	c.execute('CREATE TABLE IF NOT EXISTS likes(liker varchar(30), likee varchar(30), like_or_hate varchar(30))')
	rows = c.execute('SELECT * FROM likes WHERE liker=? AND likee=?', [liker, likee]) #check if they've already liked each other
	if rows.fetchone() is None:
		#if they have not already liked them
		try:
			response = "tried "

			c.execute('INSERT INTO likes(liker, likee, like_or_hate) VALUES(?, ?, ?)',[liker, likee, like_or_hate])
			
		except sqlite3.Error as er:
			response = " excepted "
			#shouldn't go through here since liker, likee should always be unique, not sure what to do on except??
			#c.execute('UPDATE likes SET longitude=?, latitude=?, radius=? WHERE userName=?',[longitude, latitude, radius, userName])
	
	

	
	
	if like_or_hate == 'like':
		user_row = c.execute("SELECT * FROM likes WHERE likee=? AND liker=? AND like_or_hate=?", [liker, likee, 'like'])#see if they mutually liked each other
		row = user_row.fetchone()
	
		if row is not None:
			success = "True" 
			c.execute('CREATE TABLE IF NOT EXISTS matches(user1 varchar(30), user2 varchar(30), couple_id integer primary key autoincrement)')
			user_row2 = c.execute("SELECT * FROM matches WHERE user1=? AND user2=?", [liker, likee])
			user_row3 = c.execute("SELECT * FROM matches WHERE user1=? AND user2=?", [likee, liker])
			if user_row2.fetchone() is None and user_row3.fetchone() is None:#test that there are not already matches
				try: 
					c.execute('INSERT INTO matches(user1, user2) VALUES(?,?)', [liker, likee])
				except sqlite3.Error as er:
					response=" excepted in matches portion"
				#shouldn't go here because couple should always be unique
			#create Matches table if not exists, update matches table
		else:
			success = "False"
	else:
		success = "False"#liker hates likee
	#boolean, if it's a match, return true
	#success = c.execute("")
	conn.commit()
	conn.close()
	data = []
	data = {'success': success, 'response': response}#success == if it's a match
	with open('test.txt', 'w') as outfile:
		json.dump(data, outfile)
	print json.dumps(data)



updateLikes()


