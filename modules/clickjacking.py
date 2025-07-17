
import requests

def check_clickjacking(url):
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        if "X-Frame-Options" in headers or "Content-Security-Policy" in headers:
            xfo = headers.get("X-Frame-Options", "").lower()
            csp = headers.get("Content-Security-Policy", "").lower()

            if "deny" in xfo or "sameorigin" in xfo or "frame-ancestors" in csp:
                return {
                    "status": "safe",
                    "explanation": "Clickjacking'e karşı koruma mevcut."
                }

        return {
            "status": "vulnerable",
            "explanation": "X-Frame-Options veya CSP frame-ancestors başlıkları eksik. Clickjacking riski var."
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "explanation": "Clickjacking kontrolü sırasında hata oluştu."
        }
