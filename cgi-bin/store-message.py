#!/usr/bin/env python
#!C:/Python27/python.exe

import cgitb
import os
import cgi
import sqlite3
import json

print 

cgitb.enable()

conn = sqlite3.connect('createUser.db')
conn.text_factory = str #need to change the text_factory for the images
c = conn.cursor()

parameters = cgi.FieldStorage()
message = parameters.getvalue("message");
username = parameters.getvalue("username");

c.execute('CREATE TABLE IF NOT EXISTS messages(message varchar(500), username varchar(30))')
c.execute('INSERT INTO messages(message, username) VALUES(?, ?)',[message, username])

conn.commit()
conn.close()

print