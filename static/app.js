function getExplanation(type, data) {
  const explanations = {
    sql_injection: {
      safe: "Bu site SQL enjeksiyonuna karşı güvenli.",
      vulnerable: "Bu site kullanıcıdan alınan veriyi filtrelemeden veritabanında kullandığı için SQL enjeksiyon açığına sahip."
    },
    xss: {
      safe: "XSS açığına karşı güvenli.",
      vulnerable: "Kullanıcıdan gelen veriler yeterince filtrelenmiyor. Bu durum zararlı script çalışmasına yol açabilir."
    },
    waf: {
      "not_detected": "WAF (Web Application Firewall) bulunamadı.",
      "detected": "Muhtemelen bir WAF (Web Application Firewall) tespit edildi."
    },
    open_redirect: {
      safe: "Açık yönlendirme problemi bulunamadı.",
      vulnerable: "Kötü niyetli yönlendirme yapılabilir. Bu kullanıcıyı başka bir siteye yönlendirerek kandırabilir."
    },
    cors: {
      safe: "CORS politikası düzgün yapılandırılmış.",
      vulnerable: "CORS ayarları uygun değil. Yetkisiz siteler veri çekebilir."
    },
    ssl: {
      valid: "SSL sertifikası geçerli.",
      invalid: "SSL sertifikası geçersiz veya yok. Bağlantı güvenli değil."
    },
    clickjacking: {
      safe: "Clickjacking'e karşı korumalı.",
      vulnerable: "X-Frame-Options header'ı eksik. Site iframe içinde açılabiliyor."
    },
    tech: {
      default: "Sunucu teknolojileri listelendi."
    }
  };

  const val = data.status || data.server || "default";
  const expl = explanations[type]?.[val] || explanations[type]?.default || "Bilgi yok.";
  return expl;
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
