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

def unMatch():
	print
	username = cookie['LOGIN'].value
	parameters = cgi.FieldStorage()
	matchee = parameters.getvalue("match_un")
	
	delete_stmt1 = "DELETE FROM matches WHERE user1 = '{}' AND user2 = '{}'".format(username, matchee )
	delete_stmt2 = "DELETE FROM matches WHERE user1 = '{}' AND user2 = '{}'".format(matchee, username)
	delete_stmt3 = "DELETE FROM likes WHERE liker = '{}' AND likee = '{}'".format(username, matchee)
	delete_stmt4 = "DELETE FROM likes WHERE liker = '{}' AND likee = '{}'".format(matchee, username)
	c.execute(delete_stmt4)
	c.execute(delete_stmt3)
	c.execute(delete_stmt2)
	c.execute(delete_stmt1)
	conn.commit()
	conn.close()

unMatch()