import requests

def detect_waf(url):
    try:
        res = requests.get(url, headers={"User-Agent": "sqlmap"}, timeout=5)
        if "access denied" in res.text.lower() or res.status_code in [403, 406]:
            return {"status": "detected", "message": "Possible WAF detected"}
        return {"status": "not_detected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}