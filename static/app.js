
async function scanVulnerabilities() {
  const url = document.getElementById('targetUrl').value;
  if (!url) return alert("URL giriniz.");
  const res = await fetch(`/api/vulnscan?url=${encodeURIComponent(url)}`);
  const data = await res.json();
  let html = "<h2>Sonuçlar:</h2><ul>";
  for (let [key, result] of Object.entries(data)) {
    html += `<li><b>${key}</b>: ${result.message || JSON.stringify(result)}</li>`;
  }
  html += "</ul>";
  document.getElementById("vulnResults").innerHTML = html;
}
