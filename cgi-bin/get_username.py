#!/usr/bin/env python
#!C:/Python27/python.exe

import cgitb
import sqlite3
import Cookie
import os
import json

stored_login_cookie = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie(stored_login_cookie)
data = {}
username = cookie['LOGIN'].value
data={'username': username}
print
print json.dumps(data)