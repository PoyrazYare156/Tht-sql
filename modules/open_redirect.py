
import requests
from urllib.parse import urljoin, urlparse

def scan_open_redirect(target_url):
    payloads = [
        "https://evil.com", 
        "//evil.com", 
        "/\\evil.com"
    ]

    results = []

    for payload in payloads:
        try:
            if "?" in target_url:
                test_url = f"{target_url}&next={payload}"
            else:
                test_url = f"{target_url}?next={payload}"

            response = requests.get(test_url, allow_redirects=False, timeout=5)
            location = response.headers.get("Location", "")

            if any(evil in location for evil in ["evil.com", "//evil.com"]):
                return {
                    "status": "vulnerable",
                    "explanation": f"Açık yönlendirme tespit edildi: {location}"
                }

            results.append(location)

        except requests.RequestException as e:
            continue  # Hatalı URL geçilecek

    return {
        "status": "safe",
        "explanation": "Yönlendirme açığı tespit edilmedi."
    }
