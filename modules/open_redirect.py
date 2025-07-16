import requests

def test_open_redirect(url):
    try:
        payload_url = f"{url}?next=http://evil.com"
        res = requests.get(payload_url, allow_redirects=False, timeout=5)
        if res.status_code in [301, 302] and "evil.com" in res.headers.get("Location", ""):
            return {"status": "vulnerable"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    return {"status": "safe"}