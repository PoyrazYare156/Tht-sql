import requests

COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "test", "dev", "admin", "api", "beta", "blog", "vpn"
]

def scan_subdomains(domain):
    found = []
    for sub in COMMON_SUBDOMAINS:
        url = f"http://{sub}.{domain}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code < 400:
                found.append(url)
        except requests.RequestException:
            continue

    return {
        "status": "found" if found else "not_found",
        "subdomains": found
    }
