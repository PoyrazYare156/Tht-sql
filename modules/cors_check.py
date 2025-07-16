import requests

def check_cors(url):
    try:
        res = requests.get(url, headers={"Origin": "http://evil.com"}, timeout=5)
        acao = res.headers.get("Access-Control-Allow-Origin")
        if acao == "*":
            return {"status": "vulnerable", "detail": "Wildcard CORS header"}
        elif acao == "http://evil.com":
            return {"status": "vulnerable", "detail": "Reflective CORS header"}
        return {"status": "safe"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}