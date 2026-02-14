import requests


#about endpoint
def about(base_url,va_cookie):
    url = f"{base_url}" + "/api/v1/about"
    headers = {"cookie": f"va={va_cookie}","accept": "application/json"}
    request = requests.get(url, headers=headers)
    if request.status_code == 200:
        print(f"About page: {request.text}")
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
        alerts = response.json()
        return alerts
    else:
        print("Get alerts failed")
        print(f"Error code:{response.status_code}")
        return False

#bookmark endpoint
def get_bookmarks(base_url, va_cookie):
    url = f"{base_url}" + "/api/v1/bookmarks"
    headers = {"cookie": f"va={va_cookie}", "accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Found bookmarks:{response.text}")
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

