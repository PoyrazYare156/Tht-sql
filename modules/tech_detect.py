import requests

def detect_tech(url):
    try:
        res = requests.get(url, timeout=5)
        headers = res.headers
        server = headers.get("Server", "Unknown")
        powered_by = headers.get("X-Powered-By", "Unknown")
        return {"server": server, "x-powered-by": powered_by}
    except Exception as e:
        return {"status": "error", "message": str(e)}