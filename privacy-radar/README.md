# Privacy Radar

A comprehensive privacy policy analysis tool that helps users understand data collection practices and privacy risks of any website. Features a Chrome extension, web dashboard, and powerful backend API.

## What It Does

Privacy Radar analyzes website privacy policies to provide users with clear, actionable insights about data collection practices. The tool examines privacy policy text to identify what data is collected, how it's used, and what rights users have, then generates a risk score and detailed breakdown.

## Key Features

- **Instant Analysis**: Analyze any website's privacy policy in seconds
- **Risk Scoring**: Get a 0-99 risk score based on comprehensive keyword analysis
- **Detailed Breakdown**: See what data is collected, how it's used, and your rights
- **Chrome Extension**: Analyze sites directly from your browser
- **Web Dashboard**: Beautiful, responsive interface for detailed analysis
- **AI-Powered**: Optional AI analysis using OpenAI or local Ollama
- **PrivacySpy Integration**: Enhanced analysis using community-validated privacy data
- **Caching**: Fast responses with intelligent caching system
- **Privacy-First**: No data collection, runs locally

## Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.12+**: Core programming language
- **httpx**: Async HTTP client for web scraping
- **BeautifulSoup4**: HTML parsing and text extraction
- **readability**: Content extraction from web pages
- **Pydantic**: Data validation and serialization
- **uvicorn**: ASGI server for FastAPI

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Chrome Extension API**: Browser extension functionality

### AI & Analysis
- **OpenAI API**: GPT models for intelligent text analysis
- **Ollama**: Local AI model support
- **PrivacySpy API**: Community-validated privacy data
- **Custom Keyword Analysis**: Heuristic-based risk scoring

### Database & Storage
- **PostgreSQL**: Primary database for caching and storage
- **SQLAlchemy**: Python ORM for database operations
- **Alembic**: Database migration management

### Deployment
- **Docker & Docker Compose**: Containerization
- **Railway**: Cloud deployment platform
- **GitHub Actions**: CI/CD pipeline

## Quick Start

### Using Docker (Recommended)

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd privacy-radar
   cp .env.example .env
   ```

2. **Configure environment** (edit `.env`):
   ```bash
   # Optional: Add your OpenAI API key for AI analysis
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Optional: Configure local Ollama
   OLLAMA_HOST=http://localhost:11434
   ```

3. **Start services**:
   ```bash
   docker-compose up --build
   ```

4. **Load Chrome Extension**:
   - Open Chrome and go to `chrome://extensions`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `extension/` folder

5. **Access the dashboard**: Open `http://localhost:3000`

### Manual Setup

#### Backend

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   export OPENAI_API_KEY="your_key_here"  # Optional
   export OLLAMA_HOST="http://localhost:11434"  # Optional
   ```

3. **Run the server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend

1. **Install dependencies**:
   ```bash
   cd dashboard
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```

#### Chrome Extension

1. **Load the extension**:
   - Open Chrome and go to `chrome://extensions`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `extension/` folder

## Free Version

For users who want to run Privacy Radar without any costs, we provide a simplified version that doesn't require a database:

```bash
# Start the free version
python3 start_free.py
```

The free version includes:
- All core privacy analysis features
- PrivacySpy integration
- AI analysis (if API keys are provided)
- No database required
- Perfect for local development and testing

## API Endpoints

### Core Endpoints

- `POST /summarize` - Analyze a website's privacy policy
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation

### Request Format

```json
{
  "domain": "example.com",
  "candidate_urls": ["https://example.com/privacy"]
}
```

### Response Format

```json
{
  "domain": "example.com",
  "source_url": "https://example.com/privacy",
  "summary": {
    "data_collected": ["email", "location", "device"],
    "purposes": ["marketing", "analytics"],
    "sharing": "sold/shared with advertisers/partners",
    "retention": "automatic deletion",
    "user_rights": "access, delete, opt out"
  },
  "risk_score": 75.5,
  "enhanced_insights": {
    "data_source": "privacyspy",
    "privacyspy_available": true,
    "key_concerns": ["Behavioral marketing allowed"],
    "privacy_strengths": ["Strong data deletion rights"]
  }
}
```

## How It Works

### 1. Privacy Policy Discovery
The system automatically searches for privacy policies using common URL patterns:
- `/privacy`
- `/privacy-policy`
- `/terms`
- `/terms-of-service`

### 2. Content Extraction
Using advanced web scraping techniques:
- Fetches the privacy policy page
- Extracts readable text content
- Removes navigation and irrelevant content
- Handles various page structures and formats

### 3. Analysis Engine
The analysis combines multiple approaches:

**Keyword Analysis**: Scans for privacy-related terms and assigns risk scores based on:
- Data collection practices
- Third-party sharing
- User rights and controls
- Retention policies

**AI Analysis** (Optional): Uses OpenAI or local Ollama models for:
- Intelligent text understanding
- Context-aware risk assessment
- Natural language processing

**PrivacySpy Integration**: Leverages community-validated data for:
- Enhanced accuracy
- Community insights
- Verified privacy assessments

### 4. Risk Scoring
Generates a 0-99 risk score based on:
- Data collection scope and sensitivity
- Third-party sharing practices
- User control and rights
- Transparency and clarity
- Compliance with privacy regulations

## PrivacySpy Integration

Privacy Radar integrates with PrivacySpy, a community-driven privacy database, to provide enhanced analysis. This integration follows PrivacySpy's Creative Commons BY license requirements:

- Proper attribution to PrivacySpy
- Links to PrivacySpy.org for more information
- Respectful use of community data
- Compliance with licensing terms

## Development

### Project Structure

```
privacy-radar/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── main.py    # Main API endpoints
│   │   ├── scoring.py # Risk scoring algorithms
│   │   ├── extract.py # Web scraping utilities
│   │   └── privacyspy.py # PrivacySpy integration
│   └── requirements.txt
├── dashboard/         # Next.js frontend
│   ├── src/
│   │   ├── pages/     # Dashboard pages
│   │   └── components/ # React components
│   └── package.json
├── extension/         # Chrome extension
│   ├── popup.html    # Extension popup
│   ├── popup.js      # Extension logic
│   ├── content.js    # Content script
│   └── manifest.json # Extension manifest
└── docker-compose.yml # Docker configuration
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd dashboard
npm test

# Extension tests
# Load extension in Chrome and test manually
```

## Deployment

### Cloud Deployment

The project is designed to work with Railway for easy cloud deployment:

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on git push

### Local Deployment

For local development and testing:

```bash
# Start all services
docker-compose up --build

# Or start individually
python3 start_free.py  # Backend only
npm run dev           # Frontend only
```

## License

This project is open source and available under the MIT License. PrivacySpy integration follows their Creative Commons BY license requirements.

## Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Check the documentation
- Review the API docs at `/docs` endpoint

## Acknowledgments

- PrivacySpy community for privacy data
- OpenAI for AI analysis capabilities
- The privacy and security community for insights and feedback