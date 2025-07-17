
import ssl
import socket
from urllib.parse import urlparse

def check_ssl(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    port = 443

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return {
                    "status": "valid",
                    "issuer": dict(x[0] for x in cert['issuer']),
                    "subject": dict(x[0] for x in cert['subject']),
                    "notBefore": cert['notBefore'],
                    "notAfter": cert['notAfter'],
                    "explanation": "SSL sertifikası geçerli ve bağlantı güvenli."
                }
    except Exception as e:
        return {
            "status": "invalid",
            "explanation": f"SSL sertifikası geçersiz veya yok: {str(e)}"
        }
