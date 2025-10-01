export const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function toReadableProxy(url: string): string {
  // r.jina.ai returns readable text for a target URL and is CORS-friendly
  // Keep scheme in path to support both http and https targets
  return `https://r.jina.ai/${url}`;
}

async function fetchText(url: string): Promise<string> {
  try {
    const proxied = toReadableProxy(url);
    const r = await fetch(proxied, { credentials: "omit" });
    const text = await r.text();
    return text.replace(/\s+/g, " ").trim().slice(0, 100000);
  } catch {
    return "";
  }
}

function heuristicRiskScore(text: string): number {
  const t = text.toLowerCase();
  const kw: Record<string, number> = {
    "sell": 20, "third party": 12, "advertis": 10, "retain indefinitely": 10,
    "biometric": 18, "location": 10, "cookie": 6, "share": 8, "tracking": 8
  };
  const safe: Record<string, number> = {
    "do not sell": -15, "no sale": -15, "data minimization": -8,
    "delete your data": -10, "opt-out": -8, "opt out": -8, "gdpr": -5, "ccpa": -5
  };
  let score = 0;
  for (const [k, w] of Object.entries(kw)) score += (t.match(new RegExp(k, "g")) || []).length * w;
  for (const [k, w] of Object.entries(safe)) score += (t.match(new RegExp(k, "g")) || []).length * w;
  return Math.max(0, Math.min(99, score));
}

function extractSummary(text: string) {
  const t = text.toLowerCase();
  const has = (k: string) => t.includes(k);
  const data: string[] = [];
  for (const k of ["email","name","phone","location","ip","device","cookie","biometric","payment"]) {
    if (has(k)) data.push(k);
  }
  const purposes = ["ads","analytics","personalization","research","improve services","security"].filter(has);
  const sharing = (has("sell") || has("advertis") || has("share")) ? "sold/shared with advertisers" : "limited/unspecified";
  const retention = has("indefinite") ? "indefinite" : (has("30 days") ? "30 days" : (has("12 months") ? "12 months" : "unspecified"));
  const rightsKeys = ["access","delete","portability","opt-out","opt out","do not sell","limit use"];
  const rights = rightsKeys.filter(has);
  return {
    data_collected: Array.from(new Set(data)).sort(),
    purposes,
    sharing,
    retention,
    user_rights: rights.length ? Array.from(new Set(rights)).sort().join(", ") : null
  };
}

async function localHeuristicSummarize(domain: string, candidateUrls: string[]) {
  const pat = /(privacy|policy|terms|cookie)/i;

  // Allow full URLs in input
  let inputUrl: URL | null = null;
  try { if (/^https?:\/\//i.test(domain)) inputUrl = new URL(domain); } catch { /* ignore */ }
  const host = inputUrl?.hostname || domain.replace(/^https?:\/\//i, "").replace(/\/$/, "");

  // Site-specific known mappings
  const siteSpecific: Record<string, string[]> = {
    "wsj.com": ["https://www.dowjones.com/privacy-notice/"],
    "www.wsj.com": ["https://www.dowjones.com/privacy-notice/"],
    "facebook.com": ["https://www.facebook.com/privacy/policy/"],
    "www.facebook.com": ["https://www.facebook.com/privacy/policy/"],
  };

  const base = inputUrl ? [inputUrl.origin] : [`https://${host}`, `https://www.${host}`];
  const guesses = [
    "/privacy",
    "/privacy-policy",
    "/policies/privacy",
    "/legal/privacy",
    "/legal/privacy-policy",
    "/terms",
    "/terms-of-service",
    "/policies/terms",
  ];
  const guessedUrls = base.flatMap(b => guesses.map(g => `${b}${g}`));

  // Also try discovering candidate links from homepage text via proxy
  const discovered: string[] = [];
  for (const b of base) {
    try {
      const homepage = await fetchText(b);
      const re = /(https?:\/\/[^\s)]+?(privacy|policy|terms)[^\s)]*)/ig;
      const found = Array.from(homepage.matchAll(re)).map(m => m[1]);
      for (const u of found) if (pat.test(u)) discovered.push(u);
    } catch { /* ignore discovery failures */ }
  }

  const fromCandidates = (candidateUrls || []).filter(u => pat.test(u));
  const siteMap = siteSpecific[host] || [];
  const tries = [
    ...(inputUrl ? [inputUrl.toString()] : []),
    ...fromCandidates,
    ...siteMap,
    ...discovered,
    ...guessedUrls,
  ];

  let text = "";
  let picked = tries[0] || `https://${host}/privacy`;
  for (const u of tries) {
    const t = await fetchText(u);
    if (t && t.length > 800) { picked = u; text = t; break; }
    if (t && t.length > 200) { picked = u; text = t; }
  }
  if (!text) {
    picked = tries[0] || `https://${host}/privacy`;
    text = await fetchText(picked);
  }
  const summary = extractSummary(text);
  const risk_score = heuristicRiskScore(text);
  return { domain, source_url: picked, summary, risk_score };
}

export async function getSite(domain: string) {
  console.log(`[Privacy Radar] Starting analysis for: ${domain}`);
  try {
    const res = await fetch(`${API}/summarize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ domain, candidate_urls: [] })
    });
    if (!res.ok) {
      console.log(`[Privacy Radar] Backend failed: ${res.status} ${res.statusText}`);
      throw new Error(`API error: ${res.status}`);
    }
    const result = await res.json();
    console.log(`[Privacy Radar] Backend success:`, result);
    return result;
  } catch (e) {
    console.log(`[Privacy Radar] Falling back to local analysis for: ${domain}`, e);
    const result = await localHeuristicSummarize(domain, []);
    console.log(`[Privacy Radar] Local analysis result:`, result);
    return result;
  }
}
