
import requests
import time
from bs4 import BeautifulSoup

def scan_sql_injection(url):
    result = {
        "status": "safe",
        "explanation": "SQL enjeksiyonu tespit edilmedi."
    }

    payloads = [
        "'", "\"", "`", "OR 1=1", "' OR '1'='1", "1 AND 1=1", "' AND SLEEP(5)--"
    ]
    error_signatures = [
        "you have an error in your sql syntax",
        "unclosed quotation mark",
        "quoted string not properly terminated",
        "sqlstate",
        "syntax error"
    ]

    try:
        # Test GET parametreleri
        if "?" in url:
            base, params = url.split("?", 1)
            pairs = params.split("&")
            for payload in payloads:
                for i in range(len(pairs)):
                    key, _ = pairs[i].split("=")
                    test_pairs = pairs.copy()
                    test_pairs[i] = f"{key}={payload}"
                    test_url = base + "?" + "&".join(test_pairs)

                    start = time.time()
                    r = requests.get(test_url, timeout=8)
                    if time.time() - start > 5:
                        return {"status": "vulnerable", "explanation": "Zaman temelli SQL Injection (Time-Based)."}

                    if any(err in r.text.lower() for err in error_signatures):
                        return {"status": "vulnerable", "explanation": "Hata mesajı döndü, SQL Injection ihtimali yüksek."}

        # Test POST formları
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")
        forms = soup.find_all("form")

        for form in forms:
            action = form.get("action") or url
            post_url = action if action.startswith("http") else url + action
            method = form.get("method", "get").lower()
            inputs = form.find_all("input")
            data = {}

            for input_tag in inputs:
                name = input_tag.get("name")
                if not name:
                    continue
                data[name] = payloads[0]

            if method == "post":
                post_r = requests.post(post_url, data=data, timeout=10)
                if any(err in post_r.text.lower() for err in error_signatures):
                    return {"status": "vulnerable", "explanation": "POST formu üzerinden SQL Injection bulundu."}

    except Exception as e:
        return {"status": "error", "explanation": f"SQL Injection taramasında hata oluştu: {e}"}

    return result
