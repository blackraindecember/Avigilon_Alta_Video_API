from wsgiref import headers

import requests


#about endpoint
def about(base_url,va_cookie):
    url = f"{base_url}" + "/api/v1/about"
    headers = {"cookie": f"va={va_cookie}","accept": "application/json"}
    request = requests.get(url, headers=headers)
    if request.status_code == 200:
        return request.text
    else:
        print(f"About page failed, error code:{request.status_code}")


# endpoint dologin /api/v1/dologin
def dologin(base_url, username, password, code):
    url = f"{base_url}" + "/api/v1/dologin"
    payload = {"username": username, "password": password, "code": code}
    headers = {"content-type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Logged in")
        va_cookie = response.cookies.get("va")
        return va_cookie
    else:
        print("Login failed")
        print(f"Error code:{response.status_code}")
        return False

#endpoint logout /api/v1/logout
def logout(va_cookie, base_url):
    url = f"{base_url}" + "/api/v1/logout"
    headers = {"cookie": f"va={va_cookie}"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("Logged out")
    else:
        print("Logout failed")
        return False

#endpoint get alerts - not complete yet

def get_alerts(va_cookie, base_url):
    url = f"{base_url}" + "/api/v1/alerts"
    headers = {
        "cookie": f"va={va_cookie}",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        alerts = response.text
        return alerts
    else:
        print("Get alerts failed")
        print(f"Error code:{response.status_code}")
        return False

def get_alertSiteSummaries(base_url, va_cookie):
    url = f"{base_url}" + "/api/v1/alertSiteSummaries"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Found alerts summaries:")
        alertSiteSummaries = response.text
        return alertSiteSummaries
    else:
        print(f"Get alerts summaries failed, error code:{response.status_code}")


#bookmark endpoint
def get_bookmarks(base_url, va_cookie):
    url = f"{base_url}" + "/api/v1/bookmarks"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Found bookmarks")
        return response.text

    else:
        print("Get bookmarks failed")
        print(f"Error code:{response.status_code}")

def post_bookmarks(base_url, va_cookie, bookmarks): #not complete yet
    url = f"{base_url}" + "/api/v1/bookmarks"
    return True

#map endpoint:
def get_map(base_url, va_cookie):
    url = f"{base_url}" + "/api/v1/maps"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        map = response.text
        return map
    else:
        print("Get map failed")
        print(f"Error code:{response.status_code}")
        return False
def post_map(base_url, va_cookie, map): # not complete yet
    url = f"{base_url}" + "/api/v1/maps"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    return True

#Counting endpoints
def get_countingAreas(base_url, va_cookie):
    url = f"{base_url}" + "/api/v1/countingAreas"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        countingAreas = response.text
        return countingAreas
    else:
        print("Get countingAreas failed")
        print(f"Error code:{response.status_code}")

def get_countingAreas_id(base_url, va_cookie, countingArea_id):
    url = f"{base_url}" + f"/api/v1/countingAreas/{countingArea_id}"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Get countingArea OK:")
        return response.text
    else:
        print("Get countingAreas failed")
        print(f"Error code:{response.status_code}")

def get_countingAreas_id_count(base_url, va_cookie, countingArea_id):
    url = f"{base_url}" + f"/api/v1/countingAreas/{countingArea_id}/counts"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Get countingArea{countingArea_id} OK:")
        return response.text
    else:
        print("Get countingAreas failed")
        print(f"Error code:{response.status_code}")

def get_countingAreas_count_log(base_url, va_cookie, countingArea_id):
    url = f"{base_url}" + f"/api/v1/countingAreas/{countingArea_id}/logs"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Get countingAreas log OK:")
        return response.text
    else:
        print("Get countingAreas log failed")
        print(f"Error code:{response.status_code}")

def post_countingAreas_reset(base_url, va_cookie, countingAreas_id):
    url = f"{base_url}" + f"/api/v1/countingAreas/{countingAreas_id}/reset"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("Reset OK")
        return True
    else:
        print("Reset failed")
        return False
def get_countingAreas_csv(base_url, va_cookie, countingAreas_id,start_time, end_time):
    url = f"{base_url}" + f"/api/v1/countingAreas/{countingAreas_id}/csv"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    params ={
        "start": start_time,
        "end": end_time,
        "step": 3600000,  # 1 giờ (ms)
        "cumulative_in_out_values": "false",
        "time_location": "Asia/Ho_Chi_Minh"
    }
    responses = requests.get(url, headers=headers, params=params)
    if responses.status_code == 200:
        print("Get countingAreas csv OK:")
        return responses.text
    else:
        print("Get countingAreas csv failed")
        print(f"Error code:{responses.status_code}")

def get_countingAreas_json(base_url, va_cookie, countingAreas_id, start_time, end_time):
    url = f"{base_url}" + f"/api/v1/countingAreas/{countingAreas_id}/json"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    params ={
        "start": start_time,
        "end": end_time,
        "step": 3600000,  # 1 giờ (ms)
        "cumulative_in_out_values": "false",
        "time_location": "Asia/Ho_Chi_Minh"
    }
    responses = requests.get(url, headers=headers, params=params)
    if responses.status_code == 200:
        print("Get countingAreas json OK:")
        return responses.text
    else:
        print("Get countingAreas json failed")
        print(f"Error code:{responses.status_code}")

def get_countingAreaConfig(base_url, va_cookie):
    url = f"{base_url}"+ "/api/v1/countingAreaConfig"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Get countingAreaConfig OK:")
        return response.text
    else:
        print("Get countingAreaConfig failed")
        return f"Error code:{response.status_code}"

def get_countingAreaPermission(base_url, va_cookie):
    url = f"{base_url}"+ "/api/v1/countingAreaPermissions"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Get countingAreaPermission OK:")
        return response.text
    else:
        print("Get countingAreaPermission failed")
        print(f"Error code:{response.status_code}")

