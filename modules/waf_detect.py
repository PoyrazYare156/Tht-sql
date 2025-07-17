
import requests

COMMON_WAF_SIGNATURES = {
    "Cloudflare": ["cloudflare"],
    "Akamai": ["akamai", "akamai-ghost"],
    "Sucuri": ["sucuri"],
    "AWS WAF": ["aws", "waf"],
    "Imperva Incapsula": ["incap", "incapsula"],
    "F5 BIG-IP": ["bigip", "f5"],
    "Barracuda": ["barracuda"],
    "StackPath": ["stackpath"],
    "DDoS-Guard": ["ddos-guard"],
    "Microsoft Azure": ["azure", "frontdoor"],
}

def detect_waf(url):
    try:
        test_payload = "' OR 1=1 --"
        target_url = f"{url}?test={test_payload}"

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; WAFScanner/1.0)",
            "X-Scanner-Test": "WAF-Test"
        }

        response = requests.get(target_url, headers=headers, timeout=8)
        server_header = response.headers.get("Server", "").lower()
        via_header = response.headers.get("Via", "").lower()
        content = response.text.lower()

        matched = []

        for waf, signatures in COMMON_WAF_SIGNATURES.items():
            if any(sig in server_header or sig in via_header or sig in content for sig in signatures):
                matched.append(waf)

        if matched:
            return {
                "status": "detected",
                "explanation": f"WAF tespit edildi: {', '.join(matched)}"
            }
        else:
            return {
                "status": "not_detected",
                "explanation": "Herhangi bir WAF tespit edilmedi."
            }

    except Exception as e:
        return {
            "status": "unknown",
            "explanation": f"WAF taraması sırasında hata oluştu: {str(e)}"
        }
