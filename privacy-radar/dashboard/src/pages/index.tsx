import { useState } from "react";
import { getSite } from "../lib/api";

export default function Home() {
  const [domain, setDomain] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const submit = async (e:any) => {
    e.preventDefault();
    setLoading(true);
    try { 
      console.log(`[Privacy Radar] Submitting domain: ${domain}`);
      const result = await getSite(domain);
      console.log(`[Privacy Radar] Got result:`, result);
      setData(result);
    } catch (error) {
      console.error(`[Privacy Radar] Error:`, error);
      setData({ error: error.message });
    } finally { 
      setLoading(false); 
    }
  };

  return (
    <main style={{fontFamily:"system-ui",padding:24, maxWidth:800, margin:"0 auto"}}>
      <h1>Student Privacy Radar</h1>
      <form onSubmit={submit} style={{display:"flex", gap:8}}>
        <input value={domain} onChange={e=>setDomain(e.target.value)} placeholder="example.com" style={{flex:1, padding:8}}/>
        <button disabled={loading} type="submit">{loading ? "Scanning..." : "Scan"}</button>
      </form>
      {data && (
        <section style={{marginTop:24}}>
          <h3>{data.domain}</h3>
          <p><b>Risk:</b> {Math.round(data.risk_score)}</p>
          <p><b>Data:</b> {data.summary.data_collected?.join(", ") || "Unclear"}</p>
          <p><b>Purposes:</b> {data.summary.purposes?.join(", ") || "Unclear"}</p>
          <p><b>Sharing:</b> {data.summary.sharing}</p>
          <p><b>Retention:</b> {data.summary.retention}</p>
          <p><b>User Rights:</b> {data.summary.user_rights || "Unspecified"}</p>
          <p><a href={data.source_url} target="_blank">Source</a></p>
        </section>
      )}
    </main>
  );
}
