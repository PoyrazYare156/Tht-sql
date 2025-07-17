import requests

def check_crlf_injection(url):
    payload = "%0d%0aX-Injection-Test: injected"
    try:
        test_url = f"{url}?test={payload}"
        response = requests.get(test_url, timeout=5)

        # Başlıklarda 'X-Injection-Test' varsa CRLF açığı var
        if "X-Injection-Test" in response.headers:
            return {
                "status": "vulnerable",
                "explanation": "CRLF Injection açığı tespit edildi! Header'a enjekte edilen veri bulundu."
            }
    except requests.RequestException:
        return {
            "status": "error",
            "explanation": "İstek sırasında hata oluştu."
        }

    return {
        "status": "safe",
        "explanation": "CRLF Injection açığı tespit edilmedi."
    }
