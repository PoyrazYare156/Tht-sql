
import requests

def detect_tech(url):
    try:
        r = requests.get(url)
        headers = r.headers
        tech = {}
        for h in ["Server", "X-Powered-By"]:
            if h in headers:
                tech[h] = headers[h]
        return {"status": "success", "technologies": tech}
    except:
        return {"status": "error"}
