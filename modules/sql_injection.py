import requests

def test_sql_injection(url):
    payloads = ["'", "' OR '1'='1", "';--", '" OR "1"="1']
    vulnerable = False
    for payload in payloads:
        try:
            test_url = f"{url}?id={payload}"
            res = requests.get(test_url, timeout=5)
            if any(error in res.text.lower() for error in ["sql", "syntax", "mysql", "query", "database error"]):
                vulnerable = True
                break
        except Exception:
            continue
    return {"status": "vulnerable" if vulnerable else "safe"}