import requests
import socket

def check_subdomain_takeover(url):
    try:
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        ip = socket.gethostbyname(domain)
        response = requests.get(f"http://{domain}", timeout=5)

        takeover_signatures = [
            "There is no such app", "No such bucket", "You're almost there!", "Do you want to register", "project not found"
        ]

        for sig in takeover_signatures:
            if sig.lower() in response.text.lower():
                return {
                    "status": "vulnerable",
                    "explanation": f"'{sig}' ifadesi bulundu. Subdomain takeover riski var."
                }

        return {
            "status": "safe",
            "explanation": "Herhangi bir takeover işareti bulunamadı."
        }

    except socket.gaierror:
        return {
            "status": "error",
            "explanation": "DNS çözümleme başarısız oldu. Alt alan adı mevcut olmayabilir."
        }
    except requests.RequestException:
        return {
            "status": "error",
            "explanation": "HTTP isteği başarısız oldu."
        }
