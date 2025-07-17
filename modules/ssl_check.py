
import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime

def check_ssl(url):
    result = {
        "status": "safe",
        "explanation": "SSL sertifikası geçerli.",
        "issuer": None,
        "valid_until": None,
        "days_remaining": None
    }

    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        port = 443

        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        expires = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
        now = datetime.utcnow()
        days_remaining = (expires - now).days

        result["issuer"] = cert['issuer'][0][0][1]
        result["valid_until"] = expires.strftime("%Y-%m-%d")
        result["days_remaining"] = days_remaining

        if days_remaining < 10:
            result["status"] = "vulnerable"
            result["explanation"] = f"SSL sertifikasının süresi yaklaşıyor: {days_remaining} gün kaldı."

    except Exception as e:
        result["status"] = "invalid"
        result["explanation"] = f"SSL sertifikası kontrol edilemedi veya geçersiz: {str(e)}"

    return result
