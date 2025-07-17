import requests

COMMON_ADMIN_PATHS = [
    "/admin", "/admin/login", "/administrator", "/adminpanel", "/cpanel", "/adminarea"
]

def check_admin_panel(url):
    vulnerable_panels = []

    for path in COMMON_ADMIN_PATHS:
        test_url = url.rstrip("/") + path
        try:
            response = requests.get(test_url, timeout=3)
            if response.status_code in [200, 401, 403]:
                vulnerable_panels.append(test_url)
        except requests.RequestException:
            continue

    return {
        "status": "found" if vulnerable_panels else "not_found",
        "panels": vulnerable_panels
    }
