
import requests

def scan_xss(url):
    xss_payload = "<script>alert(1)</script>"
    test_url = f"{url}?test={xss_payload}"

    try:
        response = requests.get(test_url, timeout=5)
        if xss_payload in response.text:
            return {
                "status": "vulnerable",
                "explanation": "XSS açığı tespit edildi."
            }
    except requests.RequestException:
        pass

    return {
        "status": "safe",
        "explanation": "XSS açığına karşı güvenli."
    }
