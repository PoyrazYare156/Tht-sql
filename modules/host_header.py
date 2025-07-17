import requests

def check_host_header_injection(url):
    try:
        headers = {
            "Host": "evil.com"
        }
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
        location = response.headers.get("Location", "")

        if "evil.com" in location or "evil.com" in response.text:
            return {
                "status": "vulnerable",
                "explanation": "Host Header Injection açığı mevcut. Sunucu Host başlığını filtrelemeden kullanıyor."
            }

    except requests.RequestException:
        return {
            "status": "error",
            "explanation": "Host Header kontrolü sırasında bağlantı hatası oluştu."
        }

    return {
        "status": "safe",
        "explanation": "Host Header Injection açığı tespit edilmedi."
    }
