function getExplanation(type, data) {
  const explanations = {
    sql_injection: {
      safe: "Bu site SQL enjeksiyonuna karşı güvenli.",
      vulnerable: "Veri tabanı sorguları filtrelenmediği için SQL açığı olabilir."
    },
    xss: {
      safe: "XSS açığına karşı güvenli.",
      vulnerable: "Kullanıcı girdileri filtrelenmediği için XSS açığı olabilir."
    },
    waf: {
      not_detected: "WAF tespit edilmedi.",
      detected: "Bir WAF tespit edildi. Güvenlik duvarı olabilir."
    },
    open_redirect: {
      safe: "Açık yönlendirme yok.",
      vulnerable: "Kullanıcı başka siteye yönlendirilebilir."
    },
    cors: {
      safe: "CORS ayarları güvenli.",
      vulnerable: "CORS açığı olabilir. Diğer siteler veri çekebilir."
    },
    ssl: {
      valid: "SSL sertifikası geçerli.",
      invalid: "SSL sertifikası geçersiz."
    },
    clickjacking: {
      safe: "Clickjacking'e karşı korumalı.",
      vulnerable: "X-Frame-Options eksik. iframe ile istismar edilebilir."
    },
    tech: {
      default: "Sunucu teknolojileri tespit edildi."
    }
  };

  const val = data.status || data.server || "default";
  return explanations[type]?.[val] || explanations[type]?.default || "Bilgi yok.";
}

async function scanVulnerabilities() {
  const url = document.getElementById("targetUrl").value;
  const response = await fetch(`/scan?url=${encodeURIComponent(url)}`);
  const data = await response.json();

  const resultsDiv = document.getElementById("vulnResults");
  resultsDiv.innerHTML = "<h3>Sonuçlar:</h3>";

  for (let vuln in data) {
    const status = data[vuln].status || data[vuln];
    let className = "not-detected";
    if (status === "safe" || status === "valid") className = "safe";
    else if (status === "vulnerable" || status === "invalid") className = "vulnerable";

    const explanation = getExplanation(vuln, data[vuln]);
    resultsDiv.innerHTML += `
      <div class="vuln-item ${className}">
        <strong>${vuln.toUpperCase()}</strong><br/>
        Durum: <code>${JSON.stringify(data[vuln])}</code><br/>
        Açıklama: <em>${explanation}</em>
      </div>
    `;
  }
}
