
import requests

COMMON_WAF_PATTERNS = {
    "cloudflare": ["cloudflare", "__cfduid", "cf-ray"],
    "sucuri": ["sucuri", "x-sucuri"],
    "aws": ["aws", "x-amz"],
    "akamai": ["akamai", "akamai-reputation"],
    "imperva": ["imperva", "incapsula"],
    "f5": ["bigip", "f5-"],
    "barikode": ["barracuda"],
}

def detect_waf(url):
    result = {
        "status": "not_detected",
        "explanation": "Herhangi bir WAF tespit edilmedi.",
        "server": None
    }

    try:
        payload = "' OR 1=1 --"
        test_url = f"{url}?test={payload}"
        headers = {"User-Agent": "Mozilla/5.0 (XSSScanner)"}

        response = requests.get(test_url, headers=headers, timeout=5)
        result["server"] = response.headers.get("Server", "N/A")

        # HTTP yanıt kodu şüpheli mi?
        if response.status_code in [403, 406, 501]:
            result["status"] = "detected"
            result["explanation"] = f"HTTP {response.status_code} ile WAF şüphesi var."
            return result

        # Başlıklardan WAF izi arama
        combined_headers = " ".join(response.headers.keys()).lower()
        for waf_name, patterns in COMMON_WAF_PATTERNS.items():
            if any(p in combined_headers for p in patterns):
                result["status"] = "detected"
                result["explanation"] = f"{waf_name.upper()} WAF tespit edildi."
                return result

    except requests.RequestException as e:
        result["explanation"] = f"Hata: {str(e)}"

    return result
