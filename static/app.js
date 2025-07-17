
async function scanVulnerabilities() {
  const url = document.getElementById("targetUrl").value.trim();
  if (!url) {
    alert("Lütfen bir URL girin.");
    return;
  }

  const resultsDiv = document.getElementById("vulnResults");
  resultsDiv.innerHTML = "<p>🔍 Taranıyor...</p>";

  try {
    const response = await fetch(`/api/vulnscan?url=${encodeURIComponent(url)}`);
    const data = await response.json();

    resultsDiv.innerHTML = "<h3>🛡️ Sonuçlar:</h3>";

    Object.entries(data).forEach(([vulnType, vulnData]) => {
      const status = vulnData.status || vulnData.result || vulnData.server || vulnData.error || "unknown";
      const explanation = getExplanation(vulnType, vulnData);
      let className = "error";

      if (["safe", "valid", "not_found", "disabled", "present"].includes(status)) className = "safe";
      else if (["vulnerable", "invalid", "found", "enabled", "missing"].includes(status)) className = "vulnerable";

      resultsDiv.innerHTML += `
        <div class="vuln-item ${className}">
          <strong>${vulnType.toUpperCase()}</strong><br>
          Durum: <code>${status}</code><br>
          Açıklama: <em>${explanation}</em>
        </div>
      `;
    });

  } catch (err) {
    resultsDiv.innerHTML = `<div class="vuln-item error">
      <strong>HATA</strong><br>
      <code>${err.message}</code>
    </div>`;
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
    },
    lfi_rfi: {
      safe: "LFI/RFI açığı bulunamadı.",
      vulnerable: "Dosya dahil etme yoluyla sistem tehlikeye atılabilir."
    },
    directory_traversal: {
      safe: "Directory Traversal açığı tespit edilmedi.",
      vulnerable: "Klasör geçiş açığı bulundu. Sunucu dosyasına erişilebiliyor."
    },
    admin_panel: {
      found: "Yönetim paneli bulundu. Yetkisiz erişim riski olabilir.",
      not_found: "Yönetim paneli tespit edilemedi."
    },
    crlf: {
      safe: "CRLF Injection açığı tespit edilmedi.",
      vulnerable: "Header'a veri enjekte edilebiliyor!",
      error: "CRLF testi sırasında hata oluştu."
    },
    directory_listing: {
      safe: "Directory Listing açığı bulunamadı.",
      vulnerable: "Sunucu dizin içeriği listeleniyor!",
      error: "Directory Listing kontrolü sırasında hata oluştu."
    },
    host_header: {
      safe: "Host Header Injection bulunamadı.",
      vulnerable: "Host başlığı filtrelenmiyor.",
      error: "Host Header kontrolü sırasında hata oluştu."
    },
    csp: {
      present: "CSP başlığı mevcut. XSS'e karşı ek bir koruma sağlar.",
      missing: "CSP başlığı eksik. Bu durum XSS riskini artırabilir.",
      error: "CSP kontrolü sırasında hata oluştu."
    },
    subdomain_takeover: {
      safe: "Alt alan adı takeover riskine karşı güvenli.",
      vulnerable: "Subdomain takeover riski tespit edildi!",
      error: "Alt alan adı kontrolü sırasında hata oluştu."
    },
    dir_listing: {
      enabled: "Dizin listeleme aktif. Saldırganlar sistem içeriğini görebilir.",
      disabled: "Dizin listeleme kapalı."
    },
    subdomains: {
      found: "Alt alan adları bulundu.",
      not_found: "Alt alan adı bulunamadı."
    },
    admin_panels: {
      found: "Yönetici paneli erişilebilir durumda.",
      not_found: "Yönetici paneli tespit edilemedi."
    }
  };

  const val = data.status || data.result || data.server || "default";
  return explanations[type]?.[val] || "Açıklama bulunamadı.";
}
