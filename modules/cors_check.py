
import requests

def check_cors(url):
    try:
        headers = {
            "Origin": "https://evil.com"
        }
        response = requests.get(url, headers=headers, timeout=5)

        allow_origin = response.headers.get("Access-Control-Allow-Origin", "")
        allow_credentials = response.headers.get("Access-Control-Allow-Credentials", "")

        if allow_origin == "*" and allow_credentials.lower() == "true":
            return {
                "status": "vulnerable",
                "explanation": "CORS yapılandırması tehlikeli: '*' ile birlikte 'Allow-Credentials: true' kullanılmış."
            }

        elif allow_origin == "https://evil.com":
            return {
                "status": "vulnerable",
                "explanation": "Kötü amaçlı 'Origin' kabul edildi. CORS güvenlik açığı olabilir."
            }

        elif allow_origin:
            return {
                "status": "safe",
                "origin": allow_origin,
                "explanation": "CORS başlığı tanımlanmış ve güvenli şekilde yapılandırılmış."
            }

        else:
            return {
                "status": "safe",
                "explanation": "CORS başlığı bulunamadı. Bu durum bazı durumlarda güvenli kabul edilir."
            }

    except requests.RequestException as e:
        return {
            "status": "error",
            "explanation": f"İstek sırasında hata oluştu: {str(e)}"
        }
