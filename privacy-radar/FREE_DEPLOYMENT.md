# 🆓 **100% FREE Privacy Radar Deployment**

This guide shows you how to run Privacy Radar completely free with AI analysis!

## 🎯 **Free Options Summary**

| Option | Cost | Setup Time | AI Analysis | Privacy | Best For |
|--------|------|------------|-------------|---------|----------|
| **Local Development** | $0 | 2 minutes | ✅ (with API key) | ⭐⭐⭐⭐⭐ | Development |
| **Railway Free Tier** | $0 | 5 minutes | ✅ (with API key) | ⭐⭐⭐ | Production |
| **Render Free Tier** | $0 | 5 minutes | ✅ (with API key) | ⭐⭐⭐ | Production |
| **Heuristic Only** | $0 | 1 minute | ❌ | ⭐⭐⭐⭐⭐ | Maximum Privacy |

## 🚀 **Option 1: Local Development (Recommended)**

**Perfect for:** Development, testing, personal use

### Quick Start (2 minutes)

```bash
# 1. Clone and setup
git clone <your-repo-url>
cd privacy-radar

# 2. Install dependencies
cd backend
python3 -m pip install -r requirements.txt

# 3. Start the free API
cd ..
python3 start_free.py
```

**That's it!** Your API is running at `http://localhost:8000`

### Optional: Add AI Analysis

```bash
# For OpenAI (recommended)
export OPENAI_API_KEY="your_openai_key_here"
python3 start_free.py

# For local Ollama
export OLLAMA_HOST="http://localhost:11434"
python3 start_free.py
```

### Test the API

```bash
# Test with any domain
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"domain": "google.com", "candidate_urls": []}'
```

---

## ☁️ **Option 2: Free Cloud Hosting**

### Railway (Recommended - $0/month)

1. **Fork this repository** to your GitHub
2. **Go to [Railway.app](https://railway.app)**
3. **Connect GitHub** and select your repository
4. **Deploy** - Railway auto-detects Python
5. **Add environment variables:**
   ```
   OPENAI_API_KEY=your_key_here (optional)
   CORS_ORIGIN=*
   ```
6. **Update extension** with your Railway URL

**Railway gives you:**
- ✅ 500 hours/month free
- ✅ Custom domain
- ✅ Automatic deployments
- ✅ Environment variables
- ✅ Logs and monitoring

### Render (Alternative - $0/month)

1. **Create new Web Service** on [Render.com](https://render.com)
2. **Connect GitHub** repository
3. **Configure:**
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && python3 -m uvicorn app.main_free:app --host 0.0.0.0 --port $PORT`
4. **Add environment variables** (same as Railway)

---

## 🔧 **Option 3: Extension-Only (Maximum Privacy)**

**Perfect for:** Users who want complete privacy

### Setup (1 minute)

1. **Load extension** in Chrome (Developer mode)
2. **Extension works** with heuristic analysis only
3. **No backend required** - everything runs locally

### Features
- ✅ **Complete privacy** - no data leaves your machine
- ✅ **Works offline** - no internet required
- ✅ **Zero cost** - no hosting or API fees
- ✅ **Instant setup** - just load the extension

---

## 🤖 **Free AI Options**

### Option A: OpenAI Free Tier
- **Cost:** $0 (with usage limits)
- **Setup:** Get free API key from OpenAI
- **Usage:** ~$0.01 per analysis after free tier

### Option B: Local Ollama
- **Cost:** $0 (runs on your machine)
- **Setup:** Install Ollama locally
- **Usage:** Completely free, no limits

### Option C: Heuristic Only
- **Cost:** $0
- **Setup:** No setup required
- **Usage:** Keyword-based analysis

---

## 📦 **Extension Distribution (Free)**

### Chrome Web Store (Free)
1. **Package extension:**
   ```bash
   cd extension
   zip -r privacy-radar-free.zip .
   ```

2. **Upload to Chrome Web Store:**
   - Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole/)
   - Upload zip file
   - Fill in store listing
   - Submit for review

### Manual Distribution (Free)
1. **Create GitHub release** with extension zip
2. **Users download** and install manually
3. **No store fees** or approval process

---

## 🎯 **Recommended Free Setup**

### For Maximum Features (Still Free!)

```bash
# 1. Get free OpenAI API key
# Visit: https://platform.openai.com/api-keys

# 2. Deploy to Railway (free)
# Follow Railway deployment steps above

# 3. Update extension with your Railway URL
# Edit extension/popup.js

# 4. Package and distribute
# Upload to Chrome Web Store (free)
```

**Total Cost: $0**
**Setup Time: 10 minutes**
**Features: Full AI analysis + PrivacySpy integration**

---

## 🔒 **Privacy Comparison**

### Local Development
- ✅ **Complete privacy** - no external requests
- ✅ **Your own API keys** - you control usage
- ✅ **Offline capable** - works without internet

### Cloud Hosting
- ⚠️ **Data sent to your server** for analysis
- ✅ **PrivacySpy data** is public and community-validated
- ✅ **No personal data stored** permanently
- ✅ **You control** the server and data

### Extension Only
- ✅ **Maximum privacy** - everything local
- ✅ **No external dependencies**
- ✅ **Works completely offline**

---

## 🚀 **Quick Start Commands**

### Local Development
```bash
# Start free API
python3 start_free.py

# Test API
curl http://localhost:8000/health

# Test analysis
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com", "candidate_urls": []}'
```

### With AI Analysis
```bash
# Set OpenAI key
export OPENAI_API_KEY="your_key_here"

# Start with AI
python3 start_free.py
```

### Extension Testing
```bash
# Load extension in Chrome
# Go to chrome://extensions
# Enable Developer mode
# Load unpacked → Select extension/ folder
```

---

## 📞 **Support & Troubleshooting**

### Common Issues

**"uvicorn not found"**
```bash
pip install uvicorn
```

**"Module not found"**
```bash
cd backend
pip install -r requirements.txt
```

**"CORS errors"**
```bash
# Set CORS_ORIGIN=* in environment
export CORS_ORIGIN="*"
```

### Getting Help
- **API Health:** http://localhost:8000/health
- **API Docs:** http://localhost:8000/docs
- **Logs:** Check terminal output

---

## 🎉 **You're All Set!**

Your Privacy Radar is now running **100% free** with:
- ✅ **AI-powered analysis** (if API key provided)
- ✅ **PrivacySpy integration** for accuracy
- ✅ **Heuristic fallback** for offline use
- ✅ **No database required** for simplicity
- ✅ **Complete privacy options** available

**Total cost: $0** 🎯

---

**Privacy Radar** - Making privacy analysis accessible to everyone, for free! 🔒✨
