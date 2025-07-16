
def check_open_redirect(url):
    if "redirect=" in url:
        return {"status": "vulnerable"}
    return {"status": "safe"}
