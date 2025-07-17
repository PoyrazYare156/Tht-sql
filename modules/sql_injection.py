
import requests

def scan_sql_injection(target_url):
    payloads = [
        "' OR '1'='1",
        "' OR 1=1--",
        "'; WAITFOR DELAY '0:0:5'--",
        "\" OR \"\" = \"",
        "' OR '1'='1' --",
        "' OR 1=1#"
    ]

    vulnerable = False
    for payload in payloads:
        test_url = f"{target_url}?input={payload}"
        try:
            response = requests.get(test_url, timeout=7)
            if (
                any(error in response.text.lower() for error in [
                    "you have an error in your sql syntax",
                    "warning: mysql",
                    "unclosed quotation mark",
                    "sqlstate",
                    "syntax error"
                ])
                or response.status_code == 500
            ):
                vulnerable = True
                break
        except requests.exceptions.RequestException:
            continue

    return {
        "status": "vulnerable" if vulnerable else "safe",
        "explanation": (
            "Kullanıcı girdisi filtrelenmeden veritabanında kullanılıyor." if vulnerable
            else "SQL enjeksiyonuna karşı güvenli."
        )
    }
