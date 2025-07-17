
import requests

def check_cors(url):
    try:
        headers = {
            "Origin": "https://evil.com",
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=8)

        acao = response.headers.get("Access-Control-Allow-Origin", "")
        credentials = response.headers.get("Access-Control-Allow-Credentials", "")

        if acao == "*" or "evil.com" in acao.lower():
            return {
                "status": "vulnerable",
                "explanation": f"CORS ayarları zayıf. Allow-Origin: {acao}"
            }

        if acao and credentials.lower() == "true":
            return {
                "status": "vulnerable",
                "explanation": "Allow-Credentials:true ile belirli origin'e açık – bu risklidir."
            }

        if acao:
            return {
                "status": "safe",
                "explanation": f"CORS ayarları yapılandırılmış: Allow-Origin: {acao}"
            }

        return {
            "status": "safe",
            "explanation": "CORS başlığı tanımlı değil, bu da bir güvenlik önlemi olabilir."
        }

    except Exception as e:
        return {
            "status": "unknown",
            "explanation": f"CORS kontrolü başarısız: {str(e)}"
        }
