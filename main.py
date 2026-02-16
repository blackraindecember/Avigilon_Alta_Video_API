import json
from  avigilon_alta_lib import *
from utils import *
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

#Login & get va cookies
va_cookie = dologin(base_url, username, password, code)
print(va_cookie)


mapid = map_counting_area_name_id(get_countingAreas(base_url,va_cookie))
print(beautify_json_v1(mapid))
#print(beautify_json(get_countingAreas_id(base_url,va_cookie,"5919b60d-aaa5-4c05-a404-125cc9996b7e")))
#print(beautify_json(get_countingAreas_id_count(base_url,va_cookie,"5919b60d-aaa5-4c05-a404-125cc9996b7e")))
#print(beautify_json(get_countingAreas_count_log(base_url,va_cookie,"5919b60d-aaa5-4c05-a404-125cc9996b7e")))

logout = logout(va_cookie, base_url)
#=======================================================================================================================