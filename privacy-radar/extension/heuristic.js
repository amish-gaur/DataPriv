async function fetchText(url) {
  try {
    const r = await fetch(url, { credentials: "omit" });
    const html = await r.text();
    const doc = new DOMParser().parseFromString(html, "text/html");
    // Prefer main/article, else body text
    const main = doc.querySelector("main, article") || doc.body;
    const text = main.innerText.replace(/\s+/g, " ").trim();
    return text.slice(0, 50000); // guard size
  } catch (e) {
    return "";
  }
}

function heuristicRiskScore(text) {
  const t = text.toLowerCase();
  const kw = {
    "sell": 20, "third party": 12, "advertis": 10, "retain indefinitely": 10,
    "biometric": 18, "location": 10, "cookie": 6, "share": 8, "tracking": 8
  };
  const safe = {
    "do not sell": -15, "no sale": -15, "data minimization": -8,
    "delete your data": -10, "opt-out": -8, "opt out": -8, "gdpr": -5, "ccpa": -5
  };
  let score = 0;
  for (const [k, w] of Object.entries(kw)) score += (t.match(new RegExp(k, "g"))||[]).length * w;
  for (const [k, w] of Object.entries(safe)) score += (t.match(new RegExp(k, "g"))||[]).length * w;
  return Math.max(0, Math.min(99, score));
}

function extractSummary(text) {
  const t = text.toLowerCase();
  const has = k => t.includes(k);
  const data = [];
  for (const k of ["email","name","phone","location","ip","device","cookie","biometric","payment"]) {
    if (has(k)) data.push(k);
  }
  const purposes = ["ads","analytics","personalization","research","improve services","security"].filter(has);
  const sharing = (has("sell") || has("advertis") || has("share")) ? "sold/shared with advertisers" : "limited/unspecified";
  const retention = has("indefinite") ? "indefinite" : (has("30 days") ? "30 days" : (has("12 months") ? "12 months" : "unspecified"));
  const rightsKeys = ["access","delete","portability","opt-out","opt out","do not sell","limit use"]; 
  const rights = rightsKeys.filter(has);
  return {
    data_collected: [...new Set(data)].sort(),
    purposes,
    sharing,
    retention,
    user_rights: rights.length ? [...new Set(rights)].sort().join(", ") : null
  };
}

async function localHeuristicSummarize(domain, candidateUrls) {
  // choose first candidate with privacy-like pattern or guess /privacy
  const pat = /(privacy|policy|terms|cookie)/i;
  const first = (candidateUrls||[]).find(u => pat.test(u)) || `https://${domain}/privacy`;
  const text = await fetchText(first);
  const summary = extractSummary(text);
  const risk = heuristicRiskScore(text);
  return { domain, source_url: first, summary, risk_score: risk };
}


