const API = "http://localhost:8000";
async function summarize(domain, links) {
  try {
    const r = await fetch(`${API}/summarize`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ domain, candidate_urls: links })
    });
    if (!r.ok) throw new Error(`API ${r.status}`);
    return await r.json();
  } catch (e) {
    // Fallback to local heuristic summarizer (no API key required)
    return await localHeuristicSummarize(domain, links);
  }
}
document.getElementById("scan").onclick = async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const res = await chrome.tabs.sendMessage(tab.id, { type: "GET_POLICY_LINKS" });
  const { domain, links } = res || {};
  const data = await summarize(domain, links || []);
  const s = Math.round(data.risk_score);
  chrome.runtime.sendMessage({ type: "SET_BADGE", score: s });
  document.getElementById("result").innerHTML = `
    <p class="risk">Risk Score: <span class="pill">${s}</span></p>
    <p><b>Data Collected:</b> ${data.summary.data_collected?.join(", ") || "Unclear"}</p>
    <p><b>Purposes:</b> ${data.summary.purposes?.join(", ") || "Unclear"}</p>
    <p><b>Sharing/Sale:</b> ${data.summary.sharing || "Unclear"}</p>
    <p><b>Retention:</b> ${data.summary.retention || "Unspecified"}</p>
    <p><b>User Rights:</b> ${data.summary.user_rights || "Unspecified"}</p>
    <a href="${data.source_url}" target="_blank">Source</a> |
    <a href="http://localhost:3000/site/${domain}" target="_blank">Details</a>
  `;
};
