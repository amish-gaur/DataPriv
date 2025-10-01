const API_ENDPOINTS = {
  cloud: "https://privacy-radar-api.railway.app",
  local: "http://localhost:8000",
  none: null
};

async function detectBestAPI() {
  console.log("Checking local API...");
  
  try {
    const response = await fetch(`${API_ENDPOINTS.local}/health`, { 
      method: 'GET',
      timeout: 2000 
    });
    if (response.ok) {
      console.log("Using local API");
      return API_ENDPOINTS.local;
    }
  } catch (e) {
    console.log("Local API not available:", e.message);
  }
  
  throw new Error("Privacy Radar API is not available. Please ensure the backend is running: python3 start_free.py");
}

async function summarize(domain, links) {
  const apiUrl = await detectBestAPI();
  
  if (!apiUrl) {
    throw new Error("Privacy Radar API is not available. Please ensure the backend is running or check your internet connection.");
  }
  
  try {
    const r = await fetch(`${apiUrl}/summarize`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ domain, candidate_urls: links })
    });
    if (!r.ok) throw new Error(`API ${r.status}`);
    const data = await r.json();
    
    data.api_source = apiUrl === API_ENDPOINTS.cloud ? 'cloud' : 'local';
    return data;
  } catch (e) {
    console.log(`API failed (${apiUrl}):`, e.message);
    throw new Error(`Failed to analyze privacy policy: ${e.message}`);
  }
}

function getRiskClass(score) {
  if (score <= 30) return "low";
  if (score <= 60) return "medium";
  return "high";
}

function getRiskLabel(score) {
  if (score <= 30) return "Low Risk";
  if (score <= 60) return "Medium Risk";
  return "High Risk";
}

function formatDataCollected(data) {
  if (!data || data.length === 0) return "No specific data types mentioned";
  if (data.length <= 3) return data.join(", ");
  return `${data.slice(0, 3).join(", ")} and ${data.length - 3} more`;
}

function formatPurposes(purposes) {
  if (!purposes || purposes.length === 0) return "No specific purposes mentioned";
  if (purposes.length <= 3) return purposes.join(", ");
  return `${purposes.slice(0, 3).join(", ")} and ${purposes.length - 3} more`;
}

function formatSharing(sharing) {
  if (!sharing) return "Not clearly specified";
  
  const sharingMap = {
    "not sold/shared": "Data is not sold or shared with third parties",
    "sold/shared with advertisers/partners": "Data may be sold or shared with advertisers and partners",
    "limited/unspecified": "Limited sharing, details not specified",
    "sold/shared": "Data is sold or shared with third parties"
  };
  
  return sharingMap[sharing] || sharing;
}

function formatRetention(retention) {
  if (!retention) return "Not specified";
  
  const retentionMap = {
    "automatic deletion": "Data is automatically deleted after a period",
    "unspecified": "Retention period not clearly specified",
    "permanent": "Data may be retained indefinitely"
  };
  
  return retentionMap[retention] || retention;
}

function formatUserRights(rights) {
  if (!rights) return "User rights not clearly specified";
  
  const rightsList = rights.split(", ");
  const rightsMap = {
    "access": "View your data",
    "delete": "Delete your data", 
    "correct": "Correct your data",
    "opt out": "Opt out of data collection",
    "opt-out": "Opt out of data collection",
    "do not sell": "Request data not be sold",
    "limit use": "Limit how data is used",
    "update": "Update your data",
    "consent": "Withdraw consent"
  };
  
  const formattedRights = rightsList.map(right => rightsMap[right] || right);
  return formattedRights.join(", ");
}

function formatInsights(enhancedInsights) {
  if (!enhancedInsights) return "";
  
  const concerns = enhancedInsights.key_concerns || [];
  const strengths = enhancedInsights.privacy_strengths || [];
  
  if (concerns.length === 0 && strengths.length === 0) return "";
  
  let html = '<div class="insights-section">';
  html += '<div class="insights-title">🔍 Privacy Analysis</div>';
  html += '<div class="insights-list">';
  
  concerns.forEach(concern => {
    html += `<span class="insight-tag concern">⚠️ ${concern}</span>`;
  });
  
  strengths.forEach(strength => {
    html += `<span class="insight-tag strength">✅ ${strength}</span>`;
  });
  
  html += '</div></div>';
  return html;
}

function getAnalysisMethodText(apiSource) {
  const methods = {
    'cloud': '🤖 AI + PrivacySpy (Cloud)',
    'local': '🤖 AI + PrivacySpy (Local)',
    'blended': '🤖 AI + PrivacySpy (Enhanced)',
    'privacyspy': '📊 PrivacySpy Community Data',
    'heuristic': '📊 Basic Analysis',
    'no_policy': '⚠️ No Privacy Policy Found'
  };
  
  return methods[apiSource] || '🤖 AI Analysis';
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("scan").onclick = async () => {
    const button = document.getElementById("scan");
    const result = document.getElementById("result");
    
    button.disabled = true;
    button.textContent = "🔍 Analyzing...";
    result.innerHTML = '<div class="loading">Analyzing privacy policy and generating insights...</div>';
    
    try {
      console.log("🔍 Starting scan...");
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      console.log("📄 Current tab:", tab.url);
      
      const res = await chrome.tabs.sendMessage(tab.id, { type: "GET_POLICY_LINKS" });
      console.log("📋 Content script response:", res);
      const { domain, links } = res || {};
      
      if (!domain) {
        throw new Error("Could not detect domain");
      }
      
      const data = await summarize(domain, links || []);
      const s = Math.round(data.risk_score);
      
      chrome.runtime.sendMessage({ type: "SET_BADGE", score: s });
      
      const analysisMethod = getAnalysisMethodText(data.enhanced_insights?.data_source || data.api_source);
      
      // Special handling for sites without privacy policies
      if (data.enhanced_insights?.data_source === 'no_policy') {
        result.innerHTML = `
          <div class="risk-score high">
            <div class="risk-info">
              <span class="risk-number">${s}</span>
              <span class="risk-label">High Risk - No Privacy Policy</span>
            </div>
            <div class="analysis-method">${analysisMethod}</div>
          </div>
          
          <div class="summary-grid">
            <div class="summary-item">
              <div class="summary-label">⚠️ Privacy Policy Status</div>
              <div class="summary-value">No privacy policy found on this website</div>
            </div>
            
            <div class="summary-item">
              <div class="summary-label">🔍 What This Means</div>
              <div class="summary-value">This site doesn't have a publicly accessible privacy policy, which makes it difficult to understand how your data is collected and used.</div>
            </div>
            
            <div class="summary-item">
              <div class="summary-label">🛡️ Recommendations</div>
              <div class="summary-value">Be cautious about sharing personal information. Consider using privacy tools and limiting data sharing.</div>
            </div>
          </div>
          
          <div class="insights-section">
            <div class="insights-title">⚠️ Privacy Concerns</div>
            <div class="insights-list">
              <span class="insight-tag concern">⚠️ No privacy policy found</span>
              <span class="insight-tag concern">⚠️ Lack of transparency</span>
              <span class="insight-tag concern">⚠️ Unknown data practices</span>
            </div>
          </div>
          
          <div class="links">
            <a href="https://privacyspy.org" target="_blank" class="link">📖 Learn More</a>
            <a href="https://privacyspy.org" target="_blank" class="link">🔍 PrivacySpy</a>
          </div>
        `;
        return;
      }
      
      result.innerHTML = `
        <div class="risk-score ${getRiskClass(s)}">
          <div class="risk-info">
            <span class="risk-number">${s}</span>
            <span class="risk-label">${getRiskLabel(s)}</span>
          </div>
          <div class="analysis-method">${analysisMethod}</div>
        </div>
        
        <div class="summary-grid">
          <div class="summary-item">
            <div class="summary-label">📊 Data Collected</div>
            <div class="summary-value ${!data.summary.data_collected?.length ? 'empty' : ''}">${formatDataCollected(data.summary.data_collected)}</div>
          </div>
          
          <div class="summary-item">
            <div class="summary-label">🎯 Purposes</div>
            <div class="summary-value ${!data.summary.purposes?.length ? 'empty' : ''}">${formatPurposes(data.summary.purposes)}</div>
          </div>
          
          <div class="summary-item">
            <div class="summary-label">🤝 Data Sharing</div>
            <div class="summary-value">${formatSharing(data.summary.sharing)}</div>
          </div>
          
          <div class="summary-item">
            <div class="summary-label">⏰ Data Retention</div>
            <div class="summary-value">${formatRetention(data.summary.retention)}</div>
          </div>
          
          <div class="summary-item">
            <div class="summary-label">⚖️ Your Rights</div>
            <div class="summary-value">${formatUserRights(data.summary.user_rights)}</div>
          </div>
        </div>
        
        ${formatInsights(data.enhanced_insights)}
        
        <div class="links">
          <a href="${data.source_url}" target="_blank" class="link">📖 View Policy</a>
          <a href="http://localhost:3000/site/${domain}" target="_blank" class="link">🔍 Full Report</a>
        </div>
      `;
      
    } catch (error) {
      console.error("Error:", error);
      if (error.message.includes("API is not available")) {
        result.innerHTML = `
          <div class="error">
            <strong>❌ Privacy Radar API is not available</strong>
            <br><br>
            <strong>To fix this:</strong>
            <br>• Make sure the backend is running: <code>python3 start_free.py</code>
            <br>• Check that the API is accessible at <code>http://localhost:8000</code>
            <br>• Verify your internet connection
          </div>
        `;
      } else if (error.message.includes("Could not establish connection")) {
        result.innerHTML = `
          <div class="error">
            <strong>❌ Extension Connection Error</strong>
            <br><br>
            <strong>To fix this:</strong>
            <br>• Reload the extension in chrome://extensions
            <br>• Refresh this page (F5)
            <br>• Try scanning again
          </div>
        `;
      } else {
        result.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
      }
    } finally {
      button.disabled = false;
      button.textContent = "🔍 Scan This Site";
    }
  };
});