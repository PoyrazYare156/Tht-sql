import requests

COMMON_ADMIN_PATHS = [
    "/admin", "/admin/login", "/administrator", "/admin.php", "/admin.html",
    "/cpanel", "/admin1", "/admin2", "/adminarea", "/admincontrol"
]

def find_admin_panel(base_url):
    found = []
    for path in COMMON_ADMIN_PATHS:
        try:
            test_url = base_url.rstrip("/") + path
            response = requests.get(test_url, timeout=5)
            if response.status_code in [200, 301, 302] and "login" in response.text.lower():
                found.append(test_url)
        except Exception:
            continue

    if found:
        return {
            "status": "found",
            "panels": found,
            "explanation": f"{len(found)} adet yönetim paneli tespit edildi."
        }
    return {
        "status": "not_found",
        "explanation": "Yönetim paneli tespit edilemedi."
    }
