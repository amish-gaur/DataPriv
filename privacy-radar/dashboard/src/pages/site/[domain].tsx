import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { API } from "../../lib/api";
import Link from "next/link";

export default function SitePage() {
  const { query } = useRouter();
  const domain = (query.domain as string) || "";
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showRawData, setShowRawData] = useState(false);

  useEffect(() => {
    if (!domain) return;
    
    setLoading(true);
    setError(null);
    
    fetch(`${API}/summarize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ domain, candidate_urls: [] })
    })
    .then(r => {
      if (!r.ok) throw new Error(`API error: ${r.status}`);
      return r.json();
    })
    .then(setData)
    .catch(err => {
      console.error("Error fetching data:", err);
      setError(err.message);
    })
    .finally(() => setLoading(false));
  }, [domain]);

  const getRiskClass = (score: number) => {
    if (score <= 30) return "risk-low";
    if (score <= 60) return "risk-medium";
    return "risk-high";
  };

  const getRiskLabel = (score: number) => {
    if (score <= 30) return "Low Risk";
    if (score <= 60) return "Medium Risk";
    return "High Risk";
  };

  const getRiskIcon = (score: number) => {
    if (score <= 30) return "🟢";
    if (score <= 60) return "🟡";
    return "🔴";
  };

  const getRiskDescription = (score: number) => {
    if (score <= 30) return "This site appears to have privacy-friendly practices with minimal data collection.";
    if (score <= 60) return "This site has moderate privacy practices with some data collection and sharing.";
    return "This site has significant privacy concerns with extensive data collection and sharing.";
  };

  const getRiskRecommendations = (score: number) => {
    if (score <= 30) return [
      "✅ Good privacy practices detected",
      "✅ Minimal data collection",
      "✅ Consider reviewing specific policies for your use case"
    ];
    if (score <= 60) return [
      "⚠️ Review data collection practices",
      "⚠️ Check sharing policies carefully",
      "⚠️ Consider using privacy tools"
    ];
    return [
      "🚨 High privacy risk detected",
      "🚨 Extensive data collection",
      "🚨 Consider avoiding or using strong privacy protection"
    ];
  };

  if (!domain) return <div className="loading">Loading…</div>;
  if (loading) return (
    <div className="loading">
      <div className="loading-spinner"></div>
      <p>🔍 Scanning {domain}…</p>
      <p className="loading-subtitle">Analyzing privacy policy in detail</p>
    </div>
  );
  if (error) return <div className="error">❌ Error: {error}</div>;
  if (!data) return <div className="error">❌ No data available</div>;

  return (
    <div className="container">
      <div className="header">
        <h1>🔍 Detailed Analysis</h1>
        <p>Comprehensive privacy policy analysis for {data.domain}</p>
      </div>

      {/* Risk Overview */}
      <div className="card risk-overview">
        <div className="risk-header">
          <div className="risk-main">
            <div className={`risk-score large ${getRiskClass(data.risk_score)}`}>
              <span className="risk-icon">{getRiskIcon(data.risk_score)}</span>
              <div className="risk-details">
                <span className="risk-number">{Math.round(data.risk_score)}</span>
                <span className="risk-label">{getRiskLabel(data.risk_score)}</span>
              </div>
            </div>
            <div className="risk-description">
              <p>{getRiskDescription(data.risk_score)}</p>
            </div>
          </div>
          <div className="risk-recommendations">
            <h4>💡 Recommendations</h4>
            <ul>
              {getRiskRecommendations(data.risk_score).map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Detailed Analysis */}
      <div className="card">
        <div className="analysis-header">
          <h2>📊 Privacy Analysis Breakdown</h2>
          <p className="source-info">Source: <a href={data.source_url} target="_blank" rel="noopener noreferrer">{data.source_url}</a></p>
        </div>

        <div className="analysis-grid">
          <div className="analysis-item data-collection">
            <h4>📊 Data Collection</h4>
            <div className="data-visualization">
              {data.summary.data_collected?.length ? (
                <div className="data-tags">
                  {data.summary.data_collected.map((item: string, index: number) => (
                    <span key={index} className={`data-tag ${getDataTagClass(item)}`}>
                      {item}
                    </span>
                  ))}
                </div>
              ) : (
                <div className="no-data-detected">
                  <span className="no-data-icon">✅</span>
                  <span>No specific data types detected</span>
                </div>
              )}
            </div>
            <div className="analysis-note">
              {data.summary.data_collected?.length ? 
                `${data.summary.data_collected.length} data types detected` : 
                "Minimal data collection detected"
              }
            </div>
          </div>

          <div className="analysis-item purposes">
            <h4>🎯 Usage Purposes</h4>
            <div className="purpose-visualization">
              {data.summary.purposes?.length ? (
                <div className="purpose-tags">
                  {data.summary.purposes.map((item: string, index: number) => (
                    <span key={index} className="purpose-tag">
                      {item}
                    </span>
                  ))}
                </div>
              ) : (
                <div className="no-data-detected">
                  <span className="no-data-icon">❓</span>
                  <span>Purposes not clearly specified</span>
                </div>
              )}
            </div>
          </div>

          <div className="analysis-item sharing">
            <h4>🤝 Data Sharing</h4>
            <div className="sharing-visualization">
              <div className={`sharing-status ${getSharingClass(data.summary.sharing)}`}>
                <span className="sharing-icon">
                  {getSharingIcon(data.summary.sharing)}
                </span>
                <span className="sharing-text">{data.summary.sharing || "Not specified"}</span>
              </div>
            </div>
          </div>

          <div className="analysis-item retention">
            <h4>⏰ Data Retention</h4>
            <div className="retention-visualization">
              <div className={`retention-status ${getRetentionClass(data.summary.retention)}`}>
                <span className="retention-icon">
                  {getRetentionIcon(data.summary.retention)}
                </span>
                <span className="retention-text">{data.summary.retention || "Not specified"}</span>
              </div>
            </div>
          </div>

          <div className="analysis-item rights">
            <h4>⚖️ User Rights</h4>
            <div className="rights-visualization">
              {data.summary.user_rights ? (
                <div className="rights-list">
                  {data.summary.user_rights.split(', ').map((right: string, index: number) => (
                    <span key={index} className="right-tag">
                      ✅ {right}
                    </span>
                  ))}
                </div>
              ) : (
                <div className="no-data-detected">
                  <span className="no-data-icon">❌</span>
                  <span>User rights not clearly specified</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Raw Data Toggle */}
        <div className="raw-data-section">
          <button 
            onClick={() => setShowRawData(!showRawData)}
            className="raw-data-toggle"
          >
            {showRawData ? "Hide" : "Show"} Raw Analysis Data
          </button>
          
          {showRawData && (
            <div className="raw-data-content">
              <pre className="raw-data-json">
                {JSON.stringify(data.summary, null, 2)}
              </pre>
            </div>
          )}
        </div>

        <div className="action-buttons">
          <a href={data.source_url} target="_blank" rel="noopener noreferrer" className="action-button primary">
            📖 View Source Policy
          </a>
          <Link href="/" className="action-button secondary">
            ← Back to Home
          </Link>
          <button 
            onClick={() => navigator.share?.({ 
              title: `Privacy Analysis for ${data.domain}`, 
              text: `Risk Score: ${Math.round(data.risk_score)} - ${getRiskLabel(data.risk_score)}`, 
              url: window.location.href 
            })}
            className="action-button tertiary"
          >
            📤 Share Analysis
          </button>
        </div>
      </div>
    </div>
  );

  // Helper functions
  function getDataTagClass(item: string): string {
    const sensitive = ['biometric', 'health', 'financial', 'social security', 'ssn', 'genetic', 'dna'];
    const moderate = ['location', 'device', 'ip', 'browsing history', 'search history'];
    
    if (sensitive.some(s => item.toLowerCase().includes(s))) return 'sensitive';
    if (moderate.some(m => item.toLowerCase().includes(m))) return 'moderate';
    return 'basic';
  }

  function getSharingClass(sharing: string): string {
    if (!sharing) return 'unknown';
    if (sharing.includes('not sold') || sharing.includes('no sharing')) return 'good';
    if (sharing.includes('sold') || sharing.includes('shared')) return 'bad';
    return 'moderate';
  }

  function getSharingIcon(sharing: string): string {
    if (!sharing) return '❓';
    if (sharing.includes('not sold') || sharing.includes('no sharing')) return '✅';
    if (sharing.includes('sold') || sharing.includes('shared')) return '❌';
    return '⚠️';
  }

  function getRetentionClass(retention: string): string {
    if (!retention) return 'unknown';
    if (retention.includes('indefinite') || retention.includes('permanent')) return 'bad';
    if (retention.includes('delete') || retention.includes('30 days')) return 'good';
    return 'moderate';
  }

  function getRetentionIcon(retention: string): string {
    if (!retention) return '❓';
    if (retention.includes('indefinite') || retention.includes('permanent')) return '❌';
    if (retention.includes('delete') || retention.includes('30 days')) return '✅';
    return '⚠️';
  }
}
