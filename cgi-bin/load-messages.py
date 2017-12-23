#!/usr/bin/env python
#!C:/Python27/python.exe

import cgitb
import os
import cgi
import sqlite3
import json

cgitb.enable()

conn = sqlite3.connect('createUser.db')
conn.text_factory = str #need to change the text_factory for the images
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS messages(message varchar(500), username varchar(30))')
messages_rows = c.execute("SELECT * FROM messages").fetchall()

data = []

if messages_rows is not None:
	for row in messages_rows:
		entry = {
			'message': row[0],
			'username': row[1]
		}
		data.append(entry)
	print
	print json.dumps(data)