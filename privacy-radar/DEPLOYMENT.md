# 🚀 Privacy Radar Deployment Guide

This guide covers different deployment options for the Privacy Radar extension with AI-powered analysis.

## 📋 Deployment Options

### Option 1: Cloud-Hosted (Recommended for End Users)

**Best for:** Maximum user experience, no setup required

#### Quick Deploy to Railway (Recommended)

1. **Fork this repository** to your GitHub account

2. **Deploy to Railway:**
   - Go to [Railway.app](https://railway.app)
   - Connect your GitHub account
   - Deploy from your forked repository
   - Select the `backend` folder as the root directory

3. **Configure Environment Variables:**
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   POSTGRES_USER=radar
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_DB=radardb
   CORS_ORIGIN=*
   CACHE_TTL_DAYS=14
   ```

4. **Update Extension Configuration:**
   - Edit `extension/popup.js`
   - Replace `https://privacy-radar-api.railway.app` with your Railway URL
   - Update the cloud API endpoint

5. **Package Extension:**
   - Zip the `extension/` folder
   - Upload to Chrome Web Store

#### Alternative: Deploy to Render

1. **Create a new Web Service on Render**
2. **Connect your GitHub repository**
3. **Configure:**
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables: Same as Railway

### Option 2: Local Development Setup

**Best for:** Developers and privacy-conscious users

#### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (or Docker)

#### Setup Steps

1. **Clone and setup:**
   ```bash
   git clone <your-repo-url>
   cd privacy-radar
   cp .env.example .env
   ```

2. **Configure environment:**
   ```bash
   # Edit .env file
   OPENAI_API_KEY=your_openai_api_key_here  # Optional
   POSTGRES_USER=radar
   POSTGRES_PASSWORD=radarpass
   POSTGRES_DB=radardb
   CORS_ORIGIN=http://localhost:3000
   ```

3. **Start services:**
   ```bash
   # Using Docker (recommended)
   docker-compose up --build
   
   # Or manually
   # Terminal 1: Start database
   docker run -d --name privacy-radar-db \
     -e POSTGRES_USER=radar \
     -e POSTGRES_PASSWORD=radarpass \
     -e POSTGRES_DB=radardb \
     -p 5432:5432 postgres:15
   
   # Terminal 2: Start backend
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   
   # Terminal 3: Start dashboard
   cd dashboard
   npm install
   npm run dev
   ```

4. **Load Extension:**
   - Open Chrome → Extensions → Developer mode
   - Load unpacked → Select `extension/` folder

### Option 3: Hybrid Approach (Best of Both Worlds)

**Features:**
- Cloud API for production users
- Local fallback for privacy-conscious users
- Automatic detection and graceful degradation

#### Implementation

1. **Deploy cloud backend** (follow Option 1)
2. **Keep local setup** (follow Option 2)
3. **Extension automatically detects** which API to use:
   - Tries cloud API first
   - Falls back to local API
   - Uses heuristic analysis if no API available

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI analysis | - | Optional |
| `OLLAMA_HOST` | Local Ollama server URL | - | Optional |
| `POSTGRES_USER` | Database username | `radar` | Yes |
| `POSTGRES_PASSWORD` | Database password | - | Yes |
| `POSTGRES_DB` | Database name | `radardb` | Yes |
| `CORS_ORIGIN` | Allowed CORS origins | `*` | Yes |
| `CACHE_TTL_DAYS` | Cache expiration in days | `14` | No |

### Extension Configuration

Update `extension/popup.js` with your API endpoints:

```javascript
const API_ENDPOINTS = {
  cloud: "https://your-api-url.railway.app",  // Your cloud API
  local: "http://localhost:8000",              // Local development
  none: null                                   // Heuristic only
};
```

## 📦 Extension Distribution

### Chrome Web Store

1. **Package extension:**
   ```bash
   cd extension
   zip -r privacy-radar-extension.zip .
   ```

2. **Upload to Chrome Web Store:**
   - Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole/)
   - Upload the zip file
   - Fill in store listing details
   - Submit for review

### Manual Distribution

1. **Create distribution package:**
   ```bash
   # Create a release zip
   zip -r privacy-radar-v1.0.0.zip extension/
   ```

2. **Users can install by:**
   - Downloading the zip file
   - Extracting it
   - Loading as unpacked extension in Chrome

## 🎯 User Experience

### For End Users (Cloud Deployment)
- ✅ **Zero setup** - just install extension
- ✅ **AI-powered analysis** with your API keys
- ✅ **PrivacySpy integration** for accurate scores
- ✅ **Always up-to-date** with latest improvements

### For Privacy-Conscious Users (Local Setup)
- ✅ **Complete privacy** - no data leaves their machine
- ✅ **Full control** over AI usage and costs
- ✅ **Offline capability** with heuristic analysis
- ✅ **Custom configuration** possible

### For Developers
- ✅ **Full source code access**
- ✅ **Customizable AI prompts**
- ✅ **Extensible architecture**
- ✅ **Local development environment**

## 💰 Cost Estimation

### Cloud Deployment
- **Railway/Render:** $5-20/month
- **OpenAI API:** $0.01-0.10 per analysis (optional)
- **Total:** $5-25/month

### Local Deployment
- **Hosting:** $0 (user's machine)
- **OpenAI API:** User's own API key
- **Total:** $0-10/month (user's choice)

## 🔒 Privacy Considerations

### Cloud Deployment
- ⚠️ **Data sent to your servers** for AI analysis
- ✅ **PrivacySpy data** is public and community-validated
- ✅ **No personal data stored** permanently
- ✅ **Caching** reduces repeated API calls

### Local Deployment
- ✅ **Complete privacy** - no external data transmission
- ✅ **User controls** all AI usage and costs
- ✅ **Offline capability** with heuristic fallback
- ✅ **No dependency** on external services

## 🚀 Next Steps

1. **Choose your deployment strategy**
2. **Set up your preferred hosting platform**
3. **Configure your API keys**
4. **Update extension configuration**
5. **Test thoroughly**
6. **Package and distribute**

## 📞 Support

- **Issues:** Report bugs on GitHub
- **Documentation:** Check `/docs` endpoint
- **Health Check:** Use `/health` endpoint
- **API Docs:** Available at `/docs` when running

---

**Privacy Radar** - Making privacy policies transparent and understandable for everyone! 🔒✨
