#!/usr/bin/env python3
"""
Test script to demonstrate AI-powered vs heuristic risk scoring
"""

import asyncio
import sys
import os

# Add the backend app to the path
sys.path.append('/Users/amish/DataPrivacy/privacy-radar/backend')

from app.scoring import risk_score, enhanced_risk_score, ai_risk_score

async def test_scoring_methods():
    """Test different scoring methods on sample privacy policy text"""
    
    # Sample privacy policy text (simplified for testing)
    sample_policy = """
    Privacy Policy
    
    We collect personal information including your name, email address, location data, 
    browsing history, and device information. We use this data for advertising, 
    analytics, and to improve our services. We may share your information with 
    third-party advertisers and partners. We retain your data indefinitely unless 
    you request deletion. You have the right to opt-out of data collection and 
    request deletion of your personal information.
    
    We use cookies and tracking technologies to monitor your behavior across 
    our website and other sites. We may sell your personal information to 
    marketing companies and data brokers. We do not provide clear opt-out 
    mechanisms for all data collection activities.
    """
    
    print("🧪 Testing Privacy Risk Scoring Methods")
    print("=" * 50)
    
    # Test heuristic scoring
    print("\n📊 Heuristic Scoring (Keyword-based):")
    heuristic_score = risk_score(sample_policy)
    print(f"   Risk Score: {heuristic_score:.1f}")
    
    # Test AI scoring (will fall back to heuristic if no AI configured)
    print("\n🤖 AI-Enhanced Scoring:")
    ai_score = await enhanced_risk_score(sample_policy)
    print(f"   Risk Score: {ai_score:.1f}")
    
    # Test direct AI scoring
    print("\n🧠 Direct AI Scoring:")
    direct_ai_score = await ai_risk_score(sample_policy)
    if direct_ai_score is not None:
        print(f"   Risk Score: {direct_ai_score:.1f}")
    else:
        print("   AI scoring not available (no API keys configured)")
    
    print("\n" + "=" * 50)
    print("💡 To enable AI scoring, set one of these environment variables:")
    print("   export OPENAI_API_KEY='your_openai_key_here'")
    print("   export OLLAMA_HOST='http://localhost:11434'")
    print("\n🔧 AI scoring provides more nuanced analysis considering:")
    print("   - Context and intent of privacy practices")
    print("   - Regulatory compliance (GDPR, CCPA)")
    print("   - User control and transparency levels")
    print("   - Data sensitivity and retention policies")

if __name__ == "__main__":
    asyncio.run(test_scoring_methods())
