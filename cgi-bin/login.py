#!C:\Python.exe

import cgitb
import cgi
import sqlite3
from hashlib import sha256

cgitb.enable()

print "Content-Type: text/html"
print "Set-Cookie: userName=value"
print ""

form = cgi.FieldStorage()

userName = form["name"].value
password = form["password"].value

conn = sqlite3.connect('createUser.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS users(username varchar(30) primary key, password varchar(30))')

rows = c.execute('SELECT * FROM users WHERE username = ?', [userName])

for row in rows:
	hashed_pass = row['password']
	salt = row['timeCreated']
	test_pass = password + salt
	test_pass = sha256(test_pass.encode('ascii')).hexdigest()
	if test_pass == hashed_pass:
		# DO SOMETHING HERE
	else:
		#do something like this
		raise Exception('Incorrect username/password')


conn.commit()
conn.close()

print '''<html>
    <head>
    </head>
    <body>
        <p>'''
print "Your name: " + name

print "Your Password: " + password
'''</p>
    </body>
</html>
'''