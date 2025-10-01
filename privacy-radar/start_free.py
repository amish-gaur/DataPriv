#!/usr/bin/env python3
"""
Free Privacy Radar Startup Script
No database required - perfect for free hosting!
"""

import os
import sys
import uvicorn

# Add the backend app to the path
sys.path.append('/Users/amish/DataPrivacy/privacy-radar/backend')

def main():
    print("🚀 Starting Privacy Radar (Free Version)")
    print("=" * 50)
    print("✅ No database required")
    print("✅ AI analysis available (if API key provided)")
    print("✅ PrivacySpy integration")
    print("✅ Heuristic fallback")
    print("=" * 50)
    
    # Set default environment variables
    os.environ.setdefault("CORS_ORIGIN", "*")
    os.environ.setdefault("OPENAI_API_KEY", "")
    os.environ.setdefault("OLLAMA_HOST", "")
    
    # Check for AI configuration
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    ollama_host = os.getenv("OLLAMA_HOST", "").strip()
    
    if openai_key:
        print("🤖 OpenAI API configured - AI analysis enabled")
    elif ollama_host:
        print("🤖 Ollama configured - Local AI analysis enabled")
    else:
        print("📊 Heuristic analysis only - no AI API keys configured")
        print("💡 Set OPENAI_API_KEY or OLLAMA_HOST for AI analysis")
    
    print("\n🌐 Starting server...")
    print("📍 API: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    print("❤️  Health: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop")
    
    # Start the server
    uvicorn.run(
        "app.main_free:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
