
import requests

def detect_tech(url):
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        tech_info = {}

        # Popüler başlıklar üzerinden teknoloji tahmini
        if "Server" in headers:
            tech_info["Server"] = headers["Server"]
        if "X-Powered-By" in headers:
            tech_info["X-Powered-By"] = headers["X-Powered-By"]
        if "Set-Cookie" in headers:
            tech_info["Cookies"] = headers["Set-Cookie"]

        # Daha fazla bilgi edinmek için bazı içerik kontrolü
        if "wp-content" in response.text or "WordPress" in response.text:
            tech_info["CMS"] = "WordPress"
        elif "Joomla!" in response.text:
            tech_info["CMS"] = "Joomla"
        elif "Drupal" in response.text:
            tech_info["CMS"] = "Drupal"

        if tech_info:
            return {
                "status": "success",
                "details": tech_info
            }
        else:
            return {
                "status": "error",
                "details": "Sunucu teknolojisi belirlenemedi."
            }

    except requests.RequestException as e:
        return {
            "status": "error",
            "details": f"İstek başarısız oldu: {str(e)}"
        }
