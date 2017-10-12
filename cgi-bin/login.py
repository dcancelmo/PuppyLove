#!C:\Python27\python.exe

import cgitb
import cgi
import sqlite3

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

#c.execute('INSERT INTO users VALUES([UserName], [DogName]) VALUES(@UserName, @DogName)')
c.execute('INSERT INTO users VALUES("userName", "password")')
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