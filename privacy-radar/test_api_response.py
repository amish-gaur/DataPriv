#!/usr/bin/env python3
"""
Test script to verify API response includes enhanced insights
"""

import requests
import json

def test_api_response():
    """Test the API response structure"""
    
    print("🧪 Testing API Response Structure")
    print("=" * 50)
    
    # Test with a domain that should have PrivacySpy data
    response = requests.post(
        "http://localhost:8000/summarize",
        headers={"Content-Type": "application/json"},
        json={"domain": "google.com", "candidate_urls": []}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ API Response received")
        print(f"   Domain: {data.get('domain')}")
        print(f"   Risk Score: {data.get('risk_score')}")
        print(f"   Enhanced Insights Present: {'enhanced_insights' in data}")
        
        if 'enhanced_insights' in data:
            insights = data['enhanced_insights']
            print(f"   Data Source: {insights.get('data_source')}")
            print(f"   PrivacySpy Available: {insights.get('privacyspy_available')}")
            if insights.get('enhanced_insights'):
                print(f"   Key Concerns: {insights['enhanced_insights'].get('key_concerns', [])}")
                print(f"   Privacy Strengths: {insights['enhanced_insights'].get('privacy_strengths', [])}")
        else:
            print("❌ Enhanced insights missing from response")
            print("   Available fields:", list(data.keys()))
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"   Response: {response.text}")

if __name__ == "__main__":
    test_api_response()
