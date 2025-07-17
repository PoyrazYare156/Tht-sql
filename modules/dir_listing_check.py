import requests

def check_directory_listing(url):
    try:
        if not url.endswith("/"):
            url += "/"

        response = requests.get(url, timeout=5)

        indicators = ["Index of /", "Directory listing for", "<title>Index of", "<h1>Index of"]

        for sign in indicators:
            if sign.lower() in response.text.lower():
                return {
                    "status": "vulnerable",
                    "explanation": f"Dizin listeleme aktif: '{sign}' ifadesi bulundu."
                }

        return {
            "status": "safe",
            "explanation": "Dizin listeleme aktif değil."
        }

    except requests.RequestException as e:
        return {
            "status": "error",
            "explanation": f"İstek sırasında hata oluştu: {str(e)}"
        }
