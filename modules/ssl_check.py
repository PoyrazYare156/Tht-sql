
import ssl
import socket
from urllib.parse import urlparse

def check_ssl(url):
    try:
        hostname = urlparse(url).hostname
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(5.0)
            s.connect((hostname, 443))
        return {"status": "valid"}
    except:
        return {"status": "invalid"}
