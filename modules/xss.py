import requests
from urllib.parse import urljoin

def scan_xss(target_url):
    payload = "<script>alert('xss')</script>"
    test_param = "xss_test"
    test_url = f"{target_url}?{test_param}={payload}"

    try:
        response = requests.get(test_url, timeout=7)

        if payload.lower() in response.text.lower():
            return {
                "status": "vulnerable",
                "explanation": "XSS açığı tespit edildi. Kullanıcıdan alınan veri filtrelenmeden geri dönüyor."
            }
        else:
            return {
                "status": "safe",
                "explanation": "XSS açığı tespit edilmedi. Sayfa gelen veriyi düzgün şekilde filtreliyor."
            }

    except requests.RequestException as e:
        return {
            "status": "error",
            "explanation": f"İstek sırasında hata oluştu: {str(e)}"
        }
