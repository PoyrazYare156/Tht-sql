
import requests

def scan_sql_injection(url):
    test_payloads = ["'", "' OR '1'='1", "';--", "\" OR \"1\"=\"1"]
    vulnerable = False

    for payload in test_payloads:
        try:
            test_url = f"{url}?id={payload}"
            response = requests.get(test_url, timeout=5)
            if any(error in response.text.lower() for error in ["sql syntax", "mysql", "native client", "ora-", "unexpected end of sql command"]):
                vulnerable = True
                break
        except requests.RequestException:
            continue

    return {
        "status": "vulnerable" if vulnerable else "safe",
        "explanation": "SQL enjeksiyonuna açık!" if vulnerable else "SQL enjeksiyonuna karşı güvenli."
    }
