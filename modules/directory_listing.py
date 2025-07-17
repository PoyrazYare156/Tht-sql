import requests

def check_directory_listing(url):
    try:
        if not url.endswith("/"):
            url += "/"
        response = requests.get(url, timeout=5)
        indicators = ["Index of", "Directory listing for", "<title>Index of"]

        if any(indicator.lower() in response.text.lower() for indicator in indicators):
            return {
                "status": "vulnerable",
                "explanation": "Directory Listing (Dizin Listeleme) açığı mevcut! Sunucu dizin yapısı ifşa ediliyor."
            }
    except requests.RequestException:
        return {
            "status": "error",
            "explanation": "Dizin kontrolü sırasında bağlantı hatası oluştu."
        }

    return {
        "status": "safe",
        "explanation": "Directory Listing açığı bulunamadı."
    }
