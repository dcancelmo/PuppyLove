import cgitb
import sqlite3
import cgi

cgitb.enable()

print 'Content-Type: text/html'
print

database_name = 'puppy_love.db'
table_name = 'users'

form = cgi.FieldStorage
username = form['username'].value()

conn = sqlite3.connect(database_name)
c = conn.cursor()
print c.execute("SELECT salt FROM " + table_name + " WHERE username=?;", username)


conn.close()