import { useState, useEffect } from "react";
import { getSite } from "../lib/api";

interface SearchHistory {
  domain: string;
  riskScore: number;
  timestamp: number;
}

export default function Home() {
  const [domain, setDomain] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchHistory, setSearchHistory] = useState<SearchHistory[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  // Load search history from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('privacy-radar-history');
    if (saved) {
      setSearchHistory(JSON.parse(saved));
    }
  }, []);

  const submit = async (e: any) => {
    e.preventDefault();
    if (!domain.trim()) return;
    
    setLoading(true);
    setError(null);
    setData(null);
    
    try { 
      console.log(`[Privacy Radar] Submitting domain: ${domain}`);
      const result = await getSite(domain);
      console.log(`[Privacy Radar] Got result:`, result);
      setData(result);
      
      // Add to search history
      const newEntry: SearchHistory = {
        domain: result.domain,
        riskScore: result.risk_score,
        timestamp: Date.now()
      };
      
      const updatedHistory = [newEntry, ...searchHistory.slice(0, 9)]; // Keep last 10
      setSearchHistory(updatedHistory);
      localStorage.setItem('privacy-radar-history', JSON.stringify(updatedHistory));
      
    } catch (error: any) {
      console.error(`[Privacy Radar] Error:`, error);
      setError(error.message || "An error occurred while scanning the site");
    } finally { 
      setLoading(false); 
    }
  };

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

  const quickSearch = (quickDomain: string) => {
    setDomain(quickDomain);
  };

  const clearHistory = () => {
    setSearchHistory([]);
    localStorage.removeItem('privacy-radar-history');
  };

  return (
    <div className="container">
      <div className="header">
        <h1>🔒 Privacy Radar</h1>
        <p>Analyze any website's privacy policy and get an instant risk assessment</p>
        <div className="header-stats">
          <div className="stat">
            <span className="stat-number">{searchHistory.length}</span>
            <span className="stat-label">Sites Analyzed</span>
          </div>
          <div className="stat">
            <span className="stat-number">
              {searchHistory.length > 0 ? Math.round(searchHistory.reduce((acc, item) => acc + item.riskScore, 0) / searchHistory.length) : 0}
            </span>
            <span className="stat-label">Avg Risk Score</span>
          </div>
        </div>
      </div>

      {/* Quick Search Suggestions */}
      <div className="card quick-search">
        <h3>🚀 Quick Analysis</h3>
        <div className="quick-buttons">
          {['github.com', 'google.com', 'facebook.com', 'duckduckgo.com', 'mozilla.org'].map(site => (
            <button 
              key={site}
              onClick={() => quickSearch(site)}
              className="quick-button"
              disabled={loading}
            >
              {site}
            </button>
          ))}
        </div>
      </div>

      <div className="card">
        <form onSubmit={submit} className="search-form">
          <input 
            value={domain} 
            onChange={e => setDomain(e.target.value)} 
            placeholder="Enter domain (e.g., example.com)" 
            className="search-input"
            disabled={loading}
          />
          <button disabled={loading || !domain.trim()} type="submit" className="search-button">
            {loading ? "Scanning..." : "🔍 Scan Site"}
          </button>
        </form>

        {loading && (
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>🔍 Analyzing privacy policy...</p>
            <p className="loading-subtitle">This may take a few seconds</p>
          </div>
        )}

        {error && (
          <div className="error">
            <p>❌ {error}</p>
            <button onClick={() => setError(null)} className="error-dismiss">Dismiss</button>
          </div>
        )}

        {data && !error && (
          <div className="results">
            <div className="result-header">
              <div className="domain-info">
                <h2>{data.domain}</h2>
                <p className="source-url">Source: {data.source_url}</p>
              </div>
              <div className={`risk-score ${getRiskClass(data.risk_score)}`}>
                <span className="risk-icon">{getRiskIcon(data.risk_score)}</span>
                <div className="risk-details">
                  <span className="risk-number">{Math.round(data.risk_score)}</span>
                  <span className="risk-label">{getRiskLabel(data.risk_score)}</span>
                </div>
              </div>
            </div>

            <div className="summary-grid">
              <div className="summary-item">
                <h4>📊 Data Collected</h4>
                <div className="data-tags">
                  {data.summary.data_collected?.length ? 
                    data.summary.data_collected.map((item: string, index: number) => (
                      <span key={index} className="data-tag">{item}</span>
                    )) : 
                    <span className="no-data">No specific data types mentioned</span>
                  }
                </div>
              </div>

              <div className="summary-item">
                <h4>🎯 Purposes</h4>
                <div className="purpose-tags">
                  {data.summary.purposes?.length ? 
                    data.summary.purposes.map((item: string, index: number) => (
                      <span key={index} className="purpose-tag">{item}</span>
                    )) : 
                    <span className="no-data">Purposes not clearly specified</span>
                  }
                </div>
              </div>

              <div className="summary-item">
                <h4>🤝 Data Sharing</h4>
                <p className="sharing-status">{data.summary.sharing || "Sharing practices not clearly specified"}</p>
              </div>

              <div className="summary-item">
                <h4>⏰ Data Retention</h4>
                <p className="retention-status">{data.summary.retention || "Retention period not specified"}</p>
              </div>

              <div className="summary-item">
                <h4>⚖️ User Rights</h4>
                <p className="rights-status">{data.summary.user_rights || "User rights not clearly specified"}</p>
              </div>
            </div>

            <div className="action-buttons">
              <a href={data.source_url} target="_blank" rel="noopener noreferrer" className="action-button primary">
                📖 View Source Policy
              </a>
              <a href={`/site/${data.domain}`} className="action-button secondary">
                🔍 Detailed Analysis
              </a>
              <button 
                onClick={() => navigator.share?.({ title: `Privacy Analysis for ${data.domain}`, text: `Risk Score: ${Math.round(data.risk_score)}`, url: window.location.href })}
                className="action-button tertiary"
              >
                📤 Share Results
              </button>
            </div>
          </div>
        )}

        {/* Search History */}
        {searchHistory.length > 0 && (
          <div className="search-history">
            <div className="history-header">
              <h3>📚 Recent Analysis</h3>
              <div className="history-controls">
                <button 
                  onClick={() => setShowHistory(!showHistory)}
                  className="toggle-button"
                >
                  {showHistory ? "Hide" : "Show"} History
                </button>
                <button onClick={clearHistory} className="clear-button">Clear</button>
              </div>
            </div>
            
            {showHistory && (
              <div className="history-list">
                {searchHistory.map((item, index) => (
                  <div key={index} className="history-item" onClick={() => setDomain(item.domain)}>
                    <div className="history-domain">{item.domain}</div>
                    <div className={`history-risk ${getRiskClass(item.riskScore)}`}>
                      {getRiskIcon(item.riskScore)} {Math.round(item.riskScore)}
                    </div>
                    <div className="history-time">
                      {new Date(item.timestamp).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
