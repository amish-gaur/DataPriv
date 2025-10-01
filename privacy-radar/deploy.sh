#!/bin/bash

# Privacy Radar Deployment Script
# This script helps you deploy Privacy Radar with AI-powered analysis

set -e

echo "🚀 Privacy Radar Deployment Script"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the privacy-radar root directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists docker; then
    echo "❌ Docker is required but not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command_exists docker-compose; then
    echo "❌ Docker Compose is required but not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Privacy Radar Environment Configuration

# Database Configuration
POSTGRES_USER=radar
POSTGRES_PASSWORD=radarpass
POSTGRES_DB=radardb

# API Configuration
CORS_ORIGIN=http://localhost:3000
CACHE_TTL_DAYS=14

# AI Configuration (Optional - leave empty for heuristic-only mode)
OPENAI_API_KEY=
OLLAMA_HOST=

# Dashboard Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
    echo "✅ Created .env file with default values"
    echo "💡 Edit .env file to add your OpenAI API key for AI-powered analysis"
else
    echo "✅ .env file already exists"
fi

# Ask user for deployment type
echo ""
echo "🎯 Choose deployment type:"
echo "1) Local development (Docker Compose)"
echo "2) Production build (Docker Compose)"
echo "3) Extension only (no backend)"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "🔧 Starting local development environment..."
        docker-compose up --build
        ;;
    2)
        echo "🏗️ Building production environment..."
        docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
        echo "✅ Production environment started"
        echo "🌐 Backend API: http://localhost:8000"
        echo "🌐 Dashboard: http://localhost:3000"
        echo "📖 API Docs: http://localhost:8000/docs"
        ;;
    3)
        echo "📦 Extension-only mode selected"
        echo "✅ Extension is ready to use with heuristic analysis"
        echo "💡 Load the extension from the 'extension/' folder in Chrome"
        echo "💡 For AI analysis, you'll need to set up a backend separately"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Load the extension in Chrome (Developer mode → Load unpacked)"
echo "2. Visit any website and click the Privacy Radar icon"
echo "3. Click 'Scan This Site' to analyze the privacy policy"
echo ""
echo "🔧 Configuration:"
echo "- Edit .env file to add your OpenAI API key for AI analysis"
echo "- Check DEPLOYMENT.md for cloud deployment options"
echo ""
echo "📞 Support:"
echo "- API Health: http://localhost:8000/health"
echo "- API Docs: http://localhost:8000/docs"
echo "- Dashboard: http://localhost:3000"
