
import ssl
import socket
from urllib.parse import urlparse
import datetime

def check_ssl(url):
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        port = 443

        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

                # Geçerlilik süresi kontrolü
                not_after = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                not_before = datetime.datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
                now = datetime.datetime.utcnow()

                if now > not_after:
                    return {
                        "status": "invalid",
                        "explanation": "SSL sertifikasının süresi dolmuş."
                    }

                if now < not_before:
                    return {
                        "status": "invalid",
                        "explanation": "SSL sertifikası henüz geçerli değil."
                    }

                return {
                    "status": "valid",
                    "explanation": f"SSL geçerli. Son Geçerlilik: {not_after.strftime('%Y-%m-%d')}"
                }

    except Exception as e:
        return {
            "status": "invalid",
            "explanation": f"SSL kontrolü başarısız: {str(e)}"
        }
