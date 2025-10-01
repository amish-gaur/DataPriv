#!/usr/bin/env python3
"""
Test script to debug PrivacySpy integration
"""

import asyncio
import sys
import os

# Add the backend app to the path
sys.path.append('/Users/amish/DataPrivacy/privacy-radar/backend')

async def test_privacyspy_integration():
    """Test PrivacySpy integration directly"""
    
    from app.privacyspy import get_privacyspy_data, enhanced_risk_score_with_privacyspy
    
    print("🧪 Testing PrivacySpy Integration")
    print("=" * 50)
    
    # Test direct PrivacySpy API call
    print("\n📡 Testing PrivacySpy API directly:")
    privacyspy_data = await get_privacyspy_data("google.com")
    if privacyspy_data:
        print(f"✅ PrivacySpy data found for google.com")
        print(f"   Score: {privacyspy_data.get('score')}")
        print(f"   Name: {privacyspy_data.get('name')}")
    else:
        print("❌ No PrivacySpy data found for google.com")
    
    # Test with 1Password (known to be in PrivacySpy)
    print("\n📡 Testing with 1Password:")
    privacyspy_data = await get_privacyspy_data("1password.com")
    if privacyspy_data:
        print(f"✅ PrivacySpy data found for 1password.com")
        print(f"   Score: {privacyspy_data.get('score')}")
        print(f"   Name: {privacyspy_data.get('name')}")
    else:
        print("❌ No PrivacySpy data found for 1password.com")
    
    # Test enhanced scoring
    print("\n🤖 Testing enhanced risk scoring:")
    sample_text = "This is a sample privacy policy with some data collection practices."
    score, insights = await enhanced_risk_score_with_privacyspy(sample_text, "google.com")
    print(f"   Risk Score: {score:.1f}")
    print(f"   Data Source: {insights.get('data_source')}")
    print(f"   PrivacySpy Available: {insights.get('privacyspy_available')}")
    if insights.get('enhanced_insights'):
        print(f"   Enhanced Insights: {insights['enhanced_insights']}")

if __name__ == "__main__":
    asyncio.run(test_privacyspy_integration())
