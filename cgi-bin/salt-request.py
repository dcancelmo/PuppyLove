import cgitb
import sqlite3
import cgi

cgitb.enable()

print 'Content-Type: text/html'
print ""

database_name = 'createUser.db'
table_name = 'users'

form = cgi.FieldStorage()
username = form['username'].value

conn = sqlite3.connect(database_name)
c = conn.cursor()
print c.execute('SELECT timeCreated FROM ' + table_name + ' WHERE username=?;', username)
conn.commit()
conn.close()
