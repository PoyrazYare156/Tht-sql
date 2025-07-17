
import requests

def check_cors(url):
    result = {
        "status": "safe",
        "explanation": "CORS yapılandırması güvenli.",
        "origin": None
    }

    test_origin = "https://evil.com"

    try:
        headers = {
            "Origin": test_origin,
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=5)

        acao = response.headers.get("Access-Control-Allow-Origin")
        result["origin"] = acao

        if acao == "*" or acao == test_origin:
            result["status"] = "vulnerable"
            result["explanation"] = f"CORS yapılandırması zayıf! `Access-Control-Allow-Origin: {acao}`"

    except requests.RequestException as e:
        result["status"] = "error"
        result["explanation"] = f"Hata: {str(e)}"

    return result
