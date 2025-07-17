import requests
import re
from urllib.parse import urlparse

def check_csrf(url):
    try:
        response = requests.get(url, timeout=5)
        html = response.text.lower()

        # Yaygın CSRF token input adları
        token_patterns = [
            r'name=["\']csrf_token["\']',
            r'name=["\']_token["\']',
            r'name=["\']authenticity_token["\']',
            r'name=["\']csrfmiddlewaretoken["\']',
        ]

        found_token = any(re.search(pattern, html) for pattern in token_patterns)

        if found_token:
            return {
                "status": "safe",
                "explanation": "Formda CSRF token tespit edildi. CSRF koruması var."
            }
        else:
            return {
                "status": "vulnerable",
                "explanation": "Formda CSRF token bulunamadı. CSRF açığı olabilir."
            }

    except requests.RequestException:
        return {
            "status": "error",
            "explanation": "Siteye erişim sırasında hata oluştu. Kontrol edilemedi."
        }
