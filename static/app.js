
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

function getExplanation(type, data) {
  const explanations = {
    sql_injection: {
      safe: "SQL enjeksiyonuna karşı güvenli.",
      vulnerable: "Kullanıcı girdisi filtrelenmeden veritabanında kullanılıyor."
    },
    xss: {
      safe: "XSS açığına karşı güvenli.",
      vulnerable: "Zararlı script çalıştırılmasına karşı savunmasız."
    },
    waf: {
      not_detected: "WAF bulunamadı.",
      detected: "WAF (Web Application Firewall) tespit edildi."
    },
    open_redirect: {
      safe: "Yönlendirme açığı yok.",
      vulnerable: "Kullanıcıyı kötü niyetli bir siteye yönlendirme riski var."
    },
    cors: {
      safe: "CORS ayarları güvenli.",
      vulnerable: "CORS başlığı yanlış yapılandırılmış."
    },
    ssl: {
      valid: "SSL sertifikası geçerli.",
      invalid: "SSL sertifikası eksik veya geçersiz."
    },
    tech: {
      success: "Sunucu teknolojileri listelendi.",
      error: "Teknoloji bilgisi alınamadı."
    },
    clickjacking: {
      safe: "Clickjacking'e karşı korumalı.",
      vulnerable: "X-Frame-Options başlığı eksik."
    }
  };
  const val = data.status || data.server || "default";
  return explanations[type]?.[val] || "Açıklama bulunamadı.";
}
