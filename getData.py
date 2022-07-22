import cgi
import cgitb; 
from flask import *

form = cgi.FieldStorage('setapp') 
print(form)
print(request)
url=request.form.get('url')
print("URL",url)