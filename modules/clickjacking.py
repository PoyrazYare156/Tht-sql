
import requests

def check_clickjacking(url):
    try:
        response = requests.get(url, timeout=5)
        x_frame_options = response.headers.get("X-Frame-Options")
        csp = response.headers.get("Content-Security-Policy", "")

        if x_frame_options:
            return {
                "status": "safe",
                "header": x_frame_options,
                "explanation": "X-Frame-Options başlığı tanımlanmış."
            }
        
        if "frame-ancestors" in csp:
            return {
                "status": "safe",
                "header": csp,
                "explanation": "CSP üzerinden frame-ancestors tanımı yapılmış."
            }

        return {
            "status": "vulnerable",
            "explanation": "Clickjacking'e karşı koruma bulunamadı. X-Frame-Options veya CSP eksik."
        }

    except requests.RequestException as e:
        return {
            "status": "error",
            "explanation": f"İstek sırasında hata oluştu: {str(e)}"
        }
