import requests

def check_clickjacking(url):
    try:
        res = requests.get(url, timeout=5)
        header = res.headers.get("X-Frame-Options", "").lower()
        if header in ["deny", "sameorigin"]:
            return {"status": "safe"}
        return {"status": "vulnerable", "header": header}
    except Exception as e:
        return {"status": "error", "detail": str(e)}