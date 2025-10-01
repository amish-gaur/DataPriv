#!/bin/bash

# Privacy Radar Free Setup Script
# Sets up Privacy Radar completely free with AI analysis

set -e

echo "🆓 Privacy Radar Free Setup"
echo "=========================="
echo "✅ 100% Free - No costs required"
echo "✅ AI Analysis available (with API key)"
echo "✅ PrivacySpy integration"
echo "✅ Heuristic fallback"
echo ""

# Check if we're in the right directory
if [ ! -f "start_free.py" ]; then
    echo "❌ Error: Please run this script from the privacy-radar root directory"
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "   Please install Python 3 first: https://python.org"
    exit 1
fi

echo "🔍 Checking Python installation..."
python3 --version

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
cd backend
python3 -m pip install -r requirements.txt
cd ..

echo "✅ Dependencies installed"

# Ask about AI configuration
echo ""
echo "🤖 AI Configuration (Optional):"
echo "1) Use OpenAI API (requires API key)"
echo "2) Use local Ollama (requires Ollama installation)"
echo "3) Heuristic only (no AI, completely free)"
echo ""
read -p "Choose option (1-3): " ai_choice

case $ai_choice in
    1)
        echo ""
        read -p "Enter your OpenAI API key: " openai_key
        if [ ! -z "$openai_key" ]; then
            export OPENAI_API_KEY="$openai_key"
            echo "✅ OpenAI API key configured"
        else
            echo "⚠️  No API key provided - will use heuristic analysis"
        fi
        ;;
    2)
        echo ""
        read -p "Enter Ollama host (default: http://localhost:11434): " ollama_host
        ollama_host=${ollama_host:-http://localhost:11434}
        export OLLAMA_HOST="$ollama_host"
        echo "✅ Ollama configured: $ollama_host"
        echo "💡 Make sure Ollama is running: ollama serve"
        ;;
    3)
        echo "✅ Heuristic analysis selected - completely free!"
        ;;
    *)
        echo "⚠️  Invalid choice - using heuristic analysis"
        ;;
esac

# Set CORS for local development
export CORS_ORIGIN="*"

echo ""
echo "🚀 Starting Privacy Radar..."
echo "=========================="
echo "📍 API: http://localhost:8000"
echo "📖 Docs: http://localhost:8000/docs"
echo "❤️  Health: http://localhost:8000/health"
echo ""
echo "💡 Load the extension in Chrome:"
echo "   1. Go to chrome://extensions"
echo "   2. Enable Developer mode"
echo "   3. Load unpacked → Select 'extension/' folder"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 start_free.py
