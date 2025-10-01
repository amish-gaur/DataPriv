# 🔒 Privacy Radar Extension

A Chrome extension that analyzes website privacy policies and provides instant risk assessments using AI and community-validated data.

## ✨ Features

- **🤖 AI-Powered Analysis**: Intelligent privacy policy analysis using OpenAI or local AI
- **📊 Community Data**: Integration with PrivacySpy's expert evaluations
- **⚡ Instant Results**: Get privacy risk scores in seconds
- **🎯 Detailed Breakdown**: See what data is collected, how it's used, and your rights
- **🔄 Smart Fallback**: Works with or without AI services
- **🔒 Privacy-First**: Option to run completely locally

## 🚀 Installation

### Option 1: Chrome Web Store (Coming Soon)
- Search for "Privacy Radar" in the Chrome Web Store
- Click "Add to Chrome"
- Start analyzing privacy policies instantly!

### Option 2: Manual Installation (Developer Mode)

1. **Download the extension:**
   - Download the latest release from GitHub
   - Extract the zip file

2. **Load in Chrome:**
   - Open Chrome and go to `chrome://extensions`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the `extension/` folder

3. **Start using:**
   - Visit any website
   - Click the Privacy Radar icon in the toolbar
   - Click "Scan This Site" to analyze the privacy policy

## 🔧 Configuration

The extension automatically detects the best available analysis method:

1. **🤖 AI + PrivacySpy** (Cloud API) - Most accurate, requires internet
2. **🤖 Local AI** (Local API) - Privacy-focused, requires local setup
3. **📊 Heuristic** (Extension only) - Basic analysis, works offline

### For AI Analysis

**Cloud API (Recommended):**
- No setup required
- Uses our hosted AI service
- Most accurate results

**Local API (Privacy-focused):**
- Set up the backend locally (see main README)
- Complete privacy - no data leaves your machine
- You control AI usage and costs

## 📊 Understanding Risk Scores

- **0-30: Low Risk** 🟢 - Privacy-friendly practices
- **31-60: Medium Risk** 🟡 - Some privacy concerns
- **61-99: High Risk** 🔴 - Significant privacy risks

### Analysis Methods

- **🤖 AI + PrivacySpy**: Combines AI analysis with community-validated data
- **🤖 Local AI**: AI analysis running on your local machine
- **📊 Heuristic**: Keyword-based analysis (works offline)

## 🎯 How It Works

1. **Content Extraction**: Finds and extracts privacy policy text
2. **AI Analysis**: Uses AI to understand privacy practices intelligently
3. **Community Validation**: Cross-references with PrivacySpy's expert data
4. **Risk Scoring**: Generates a 0-99 risk score based on multiple factors
5. **Detailed Breakdown**: Shows what data is collected and how it's used

## 🔒 Privacy & Security

- **No Data Collection**: We don't collect or store your browsing data
- **Local Processing**: Option to run everything on your machine
- **Transparent Analysis**: See exactly what data is being analyzed
- **Open Source**: Full source code available for review

## 🛠️ Development

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd privacy-radar
   ```

2. **Start the backend:**
   ```bash
   docker-compose up
   ```

3. **Load the extension:**
   - Follow manual installation steps above
   - Extension will automatically detect local API

### Building for Production

1. **Update API endpoints** in `popup.js`
2. **Package the extension:**
   ```bash
   cd extension
   zip -r privacy-radar-extension.zip .
   ```

## 📞 Support

- **Issues**: Report bugs on GitHub
- **Documentation**: Check the main README
- **API Health**: http://localhost:8000/health (if running locally)

## 🤝 Contributing

We welcome contributions! Please see the main repository for contribution guidelines.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Privacy Radar** - Making privacy policies transparent and understandable for everyone! 🔒✨
