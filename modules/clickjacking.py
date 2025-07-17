
import requests

def check_clickjacking(url):
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        # X-Frame-Options kontrolü
        xfo = headers.get("X-Frame-Options", "")
        csp = headers.get("Content-Security-Policy", "")

        if "DENY" in xfo or "SAMEORIGIN" in xfo:
            return {
                "status": "safe",
                "details": "X-Frame-Options ile iframe engellenmiş."
            }
        elif "frame-ancestors" in csp and ("'none'" in csp or "'self'" in csp):
            return {
                "status": "safe",
                "details": "CSP ile iframe kontrolü mevcut."
            }
        else:
            return {
                "status": "vulnerable",
                "details": "Clickjacking'e karşı koruma başlıkları eksik."
            }

    except requests.RequestException as e:
        return {
            "status": "error",
            "details": f"Bağlantı hatası: {str(e)}"
        }
