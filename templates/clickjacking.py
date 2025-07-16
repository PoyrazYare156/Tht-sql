
import requests

def check_clickjacking(url):
    try:
        response = requests.get(url)
        if "X-Frame-Options" not in response.headers:
            return {"status": "vulnerable"}
        return {"status": "safe"}
    except:
        return {"status": "error"}
