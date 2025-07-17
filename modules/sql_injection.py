
import requests
from urllib.parse import urlparse, parse_qs, urlencode
import time

error_payloads = [
    "'",
    "\"",
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "' OR 1=1--",
    "'; WAITFOR DELAY '0:0:5'--"
]

sql_errors = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "SQLSTATE",
    "ORA-01756",
    "System.Data.SqlClient.SqlException"
]

def scan_sql_injection(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    if not query:
        return {"status": "info", "explanation": "Test edilecek parametre bulunamadı."}

    for param in query:
        for payload in error_payloads:
            test_params = query.copy()
            test_params[param] = payload
            test_query = urlencode(test_params, doseq=True)
            test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{test_query}"

            try:
                start = time.time()
                response = requests.get(test_url, timeout=7)
                duration = time.time() - start

                body = response.text.lower()
                if any(error in body for error in sql_errors):
                    return {
                        "status": "vulnerable",
                        "explanation": "SQL hatası döndü. Enjeksiyon açığı mevcut olabilir.",
                        "payload": payload,
                        "type": "error-based"
                    }

                if duration > 4.5:  # Time-based SQLi
                    return {
                        "status": "vulnerable",
                        "explanation": "Sunucu geç yanıt verdi. Time-based SQL enjeksiyonu olabilir.",
                        "payload": payload,
                        "type": "time-based"
                    }

            except requests.RequestException:
                continue

    return {
        "status": "safe",
        "explanation": "SQL enjeksiyonuna karşı güvenli."
    }
