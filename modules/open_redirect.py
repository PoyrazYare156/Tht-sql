
import requests

def scan_open_redirect(url):
    test_payload = "https://evil.com"
    redirect_url = f"{url}?next={test_payload}"

    try:
        response = requests.get(redirect_url, allow_redirects=False, timeout=5)
        if response.status_code in [301, 302] and "evil.com" in response.headers.get("Location", ""):
            return {
                "status": "vulnerable",
                "explanation": "Yönlendirme açığı tespit edildi."
            }
    except requests.RequestException:
        pass

    return {
        "status": "safe",
        "explanation": "Yönlendirme açığı yok."
    }
