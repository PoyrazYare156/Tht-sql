
import requests
import time

ERROR_PATTERNS = [
    "you have an error in your sql syntax",
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "mysql_fetch",
    "syntax error",
    "Warning: mysql",
    "SQLSTATE"
]

TIME_PAYLOADS = [
    "' OR SLEEP(5)--",
    "'; WAITFOR DELAY '0:0:5'--",
    "' || pg_sleep(5)--",
]

def scan_sql_injection(url):
    result = {
        "status": "safe",
        "explanation": "SQL enjeksiyonuna karşı güvenli.",
        "payload": None,
        "response_time": None
    }

    try:
        # Hata tabanlı payload testleri
        for payload in ["'", "'\"", "1' OR '1'='1", "' OR 'a'='a"]:
            test_url = f"{url}?test={payload}"
            response = requests.get(test_url, timeout=5)

            for pattern in ERROR_PATTERNS:
                if pattern.lower() in response.text.lower():
                    result["status"] = "vulnerable"
                    result["explanation"] = "SQL hatası döndü. Enjeksiyon açığı mevcut olabilir."
                    result["payload"] = payload
                    return result

        # Zaman tabanlı (blind SQLi) payload testleri
        for payload in TIME_PAYLOADS:
            test_url = f"{url}?id={payload}"
            start = time.time()
            requests.get(test_url, timeout=10)
            end = time.time()
            elapsed = end - start

            if elapsed > 4:  # 5 saniyelik gecikme varsa şüpheli
                result["status"] = "vulnerable"
                result["explanation"] = "Zaman tabanlı SQL enjeksiyonu açığı tespit edildi."
                result["payload"] = payload
                result["response_time"] = round(elapsed, 2)
                return result

    except requests.RequestException as e:
        result["explanation"] = f"Hata oluştu: {str(e)}"

    return result
