
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
      vulnerable: "LFI veya RFI açığı bulundu. Dosya dahil etme yoluyla sistem tehlikeye atılabilir."
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
  vulnerable: "CRLF Injection açığı bulundu! Header'a veri enjekte edilebiliyor.",
  error: "CRLF testi sırasında hata oluştu."
}
    
  };

  const val = data.status || data.server || "default";
  return explanations[type]?.[val] || "Açıklama bulunamadı.";
}
