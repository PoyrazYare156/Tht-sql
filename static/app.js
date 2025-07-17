
async function scanVulnerabilities() {
  const url = document.getElementById("targetUrl").value;
  const response = await fetch(`/api/vulnscan?url=${encodeURIComponent(url)}`);
  const data = await response.json();

  const resultsDiv = document.getElementById("vulnResults");
  resultsDiv.innerHTML = "<h3>🧪 Tespit Edilen Güvenlik Durumları:</h3>";

  for (let vuln in data) {
    const status = data[vuln].status || "unknown";
    let className = "not-detected";
    if (status === "safe" || status === "valid") className = "safe";
    else if (status === "vulnerable" || status === "invalid") className = "vulnerable";
    else if (status === "error") className = "error";

    const explanation = data[vuln].explanation || "Açıklama sağlanamadı.";

    resultsDiv.innerHTML += `
      <div class="vuln-item ${className}">
        <h4>${vuln.toUpperCase()}</h4>
        <strong>Durum:</strong> ${status}<br/>
        <strong>Açıklama:</strong> <em>${explanation}</em><br/>
      </div>
    `;
  }
}
