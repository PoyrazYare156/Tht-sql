
def scan_xss(url):
    if "<script>" in url or "alert(" in url:
        return {"status": "vulnerable", "payload": "basic script injection"}
    return {"status": "safe"}
