
import requests

def detect_tech(url):
    try:
        response = requests.get(url, timeout=5)
        server = response.headers.get("Server", "Bilinmiyor")
        powered_by = response.headers.get("X-Powered-By", "Bilinmiyor")
        content_type = response.headers.get("Content-Type", "Bilinmiyor")

        return {
            "status": "success",
            "server": server,
            "powered_by": powered_by,
            "content_type": content_type,
            "explanation": "Sunucu teknolojisi tespit edildi."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "explanation": "Sunucu teknolojisi tespit edilemedi."
        }
