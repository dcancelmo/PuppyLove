#!/usr/bin/env python
#!C:/Python27/python.exe

import cgitb
import Cookie
import datetime

cgitb.enable()

new_cookie = Cookie.SimpleCookie()
new_cookie['LOGIN'] = "0"
expires = datetime.datetime.utcnow() - datetime.timedelta(days=100)
new_cookie['LOGIN']['expires'] = expires.strftime("%a,%d%b%Y%H:%M:%SGMT")

print "Content-Type: text/html"
print new_cookie
print "Location: ../login.html"
print
print "<html><script>sessionStorage.clear()</script></html>"
