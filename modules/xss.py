import requests

def test_xss(url):
    test_param = "<script>alert(1)</script>"
    try:
        test_url = f"{url}?q={test_param}"
        response = requests.get(test_url, timeout=5)
        if test_param in response.text:
            return {"status": "vulnerable", "detail": "Payload reflected in response"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    return {"status": "safe"}