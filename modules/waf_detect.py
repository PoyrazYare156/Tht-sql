
import requests

def detect_waf(url):
    try:
        response = requests.get(url)
        server = response.headers.get("Server", "")
        if "cloudflare" in server.lower() or "waf" in server.lower():
            return {"status": "detected", "server": server}
        return {"status": "not_detected", "server": server}
    except:
        return {"status": "not_detected"}
