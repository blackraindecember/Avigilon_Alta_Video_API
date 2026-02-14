import json
from  avigilon_alta_lib import *
import os
import requests

from avigilon_alta_lib import dologin

# load config file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

base_url = config["base_url"]
username = config["username"]
password = config["password"]
code = config["code"]


va_cookie = dologin(base_url, username, password, code)
print(va_cookie)
print(about(base_url,va_cookie))
print(get_bookmarks(base_url,va_cookie))
print(get_map(base_url,va_cookie))
alert = get_alerts(va_cookie, base_url)

logout = logout(va_cookie, base_url)
#=======================================================================================================================