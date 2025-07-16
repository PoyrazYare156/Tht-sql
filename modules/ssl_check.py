import ssl
import socket
from urllib.parse import urlparse

def check_ssl(url):
    try:
        hostname = urlparse(url).hostname
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
        return {"status": "valid", "subject": cert.get("subject", [])}
    except Exception as e:
        return {"status": "invalid", "error": str(e)}