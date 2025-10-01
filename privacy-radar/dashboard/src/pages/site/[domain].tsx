import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { API } from "../../lib/api";

export default function SitePage() {
  const { query } = useRouter();
  const domain = (query.domain as string) || "";
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    if (!domain) return;
    fetch(`${API}/summarize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ domain, candidate_urls: [] })
    }).then(r => r.json()).then(setData);
  }, [domain]);

  if (!domain) return <p>Loading…</p>;
  if (!data) return <p>Scanning {domain}…</p>;

  return (
    <main style={{fontFamily:"system-ui",padding:24, maxWidth:900, margin:"0 auto"}}>
      <h1>{data.domain}</h1>
      <p>Risk: {Math.round(data.risk_score)}</p>
      <pre style={{whiteSpace:"pre-wrap", background:"#fafafa", padding:16, border:"1px solid #eee"}}>
{JSON.stringify(data.summary, null, 2)}
      </pre>
      <a href={data.source_url} target="_blank">View Source</a>
    </main>
  );
}
