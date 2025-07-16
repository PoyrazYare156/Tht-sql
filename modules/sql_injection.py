
def scan_sql_injection(url):
    if "'" in url or "--" in url:
        return {"status": "vulnerable", "vector": "simple SQL injection pattern"}
    return {"status": "safe"}
