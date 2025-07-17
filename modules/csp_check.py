import requests

def check_csp(url):
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        if "Content-Security-Policy" in headers:
            return {
                "status": "present",
                "policy": headers["Content-Security-Policy"],
                "explanation": "CSP başlığı mevcut."
            }
        else:
            return {
                "status": "missing",
                "explanation": "Content-Security-Policy başlığı bulunamadı."
            }

    except requests.RequestException:
        return {
            "status": "error",
            "explanation": "CSP kontrolü sırasında bağlantı hatası oluştu."
        }
