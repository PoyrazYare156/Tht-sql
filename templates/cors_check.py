
import requests

def check_cors(url):
    try:
        response = requests.get(url)
        if "Access-Control-Allow-Origin" in response.headers:
            if "*" in response.headers["Access-Control-Allow-Origin"]:
                return {"status": "vulnerable"}
        return {"status": "safe"}
    except:
        return {"status": "error"}
