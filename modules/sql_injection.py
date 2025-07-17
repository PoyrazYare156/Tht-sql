
import requests
import time

def scan_sql_injection(url):
    result = {
        "status": "safe",
        "explanation": "SQL enjeksiyonu tespit edilmedi."
    }

    payloads = [
        "'", "\"", "`", "OR 1=1", "' OR '1'='1", "\" OR \"1\"=\"1", "1 AND 1=1", "1 AND 1=2", "' AND SLEEP(5)--", "\" AND SLEEP(5)--"
    ]
    error_keywords = [
        "you have an error in your sql syntax",
        "unclosed quotation mark",
        "quoted string not properly terminated",
        "mysql_fetch",
        "syntax error",
        "sqlstate"
    ]

    try:
        for payload in payloads:
            # Append payload to query param
            test_url = url
            if "?" not in url:
                continue
            base, params = url.split("?", 1)
            param_pairs = params.split("&")
            for i, pair in enumerate(param_pairs):
                if "=" in pair:
                    key, _ = pair.split("=", 1)
                    test_params = param_pairs.copy()
                    test_params[i] = f"{key}={payload}"
                    new_url = base + "?" + "&".join(test_params)
                    
                    # Time-based test
                    start = time.time()
                    r = requests.get(new_url, timeout=7)
                    elapsed = time.time() - start

                    if elapsed > 5:
                        result["status"] = "vulnerable"
                        result["explanation"] = "Zaman temelli SQL Injection tespit edildi (Time-Based)."
                        return result

                    # Error-based test
                    if any(err in r.text.lower() for err in error_keywords):
                        result["status"] = "vulnerable"
                        result["explanation"] = "SQL hatası döndü. Enjeksiyon açığı mevcut olabilir."
                        return result

        return result

    except Exception as e:
        return {
            "status": "error",
            "explanation": f"SQL Injection taraması sırasında hata oluştu: {str(e)}"
        }
