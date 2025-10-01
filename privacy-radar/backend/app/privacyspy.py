import httpx
import json
from typing import Optional, Dict, Any
import asyncio

PRIVACYSPY_BASE_URL = "https://privacyspy.org/api/v2"
PRIVACYSPY_ATTRIBUTION = "Data provided by PrivacySpy (https://privacyspy.org) under Creative Commons BY license"

class PrivacySpyClient:
    def __init__(self):
        self.base_url = PRIVACYSPY_BASE_URL
        self.cache = {}
        self.cache_ttl = 3600
    
    async def get_product_by_domain(self, domain: str) -> Optional[Dict[str, Any]]:
        domain = domain.lower().strip()
        if domain.startswith(('http://', 'https://')):
            from urllib.parse import urlparse
            domain = urlparse(domain).hostname or domain
        
        cache_key = f"domain:{domain}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if asyncio.get_event_loop().time() - timestamp < self.cache_ttl:
                return cached_data
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/products/{domain}")
                if response.status_code == 200:
                    data = response.json()
                    self.cache[cache_key] = (data, asyncio.get_event_loop().time())
                    return data
        except Exception as e:
            print(f"PrivacySpy API error for {domain}: {e}")
        
        return None
    
    def convert_privacyspy_score_to_risk(self, privacyspy_score: float) -> float:
        if privacyspy_score is None:
            return 50.0
        
        privacyspy_score = float(privacyspy_score)
        
        if privacyspy_score >= 8.0:
            return 0.0
        elif privacyspy_score >= 6.0:
            return 20.0
        elif privacyspy_score >= 4.0:
            return 40.0
        elif privacyspy_score >= 2.0:
            return 60.0
        else:
            return 80.0
    
    def extract_enhanced_insights(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        insights = {
            "data_sensitivity": "medium",
            "user_control": "medium",
            "transparency": "medium",
            "compliance": "medium",
            "key_concerns": [],
            "privacy_strengths": []
        }
        
        if not product_data or "rubric" not in product_data:
            return insights
        
        rubric = product_data["rubric"]
        
        for item in rubric:
            question = item.get("question", {})
            option = item.get("option", {})
            category = question.get("category", "")
            slug = question.get("slug", "")
            percent = option.get("percent", 0)
            
            if category == "collection":
                if slug == "data-collection-reasoning" and percent < 50:
                    insights["transparency"] = "low"
                elif slug == "list-collected" and percent < 50:
                    insights["transparency"] = "low"
                elif slug == "noncritical-purposes" and percent < 50:
                    insights["user_control"] = "low"
                    
            elif category == "handling":
                if slug == "behavioral-marketing" and percent < 50:
                    insights["key_concerns"].append("Behavioral marketing allowed")
                elif slug == "third-party-access" and percent < 50:
                    insights["key_concerns"].append("Extensive third-party data sharing")
                elif slug == "data-deletion" and percent >= 80:
                    insights["privacy_strengths"].append("Strong data deletion rights")
                    
            elif category == "transparency":
                if slug == "security" and percent >= 80:
                    insights["privacy_strengths"].append("Strong security practices")
                elif slug == "history" and percent >= 80:
                    insights["privacy_strengths"].append("Policy change transparency")
                elif slug == "data-breaches" and percent >= 80:
                    insights["privacy_strengths"].append("Data breach notification")
        
        return insights

privacyspy_client = PrivacySpyClient()

async def get_privacyspy_data(domain: str) -> Optional[Dict[str, Any]]:
    return await privacyspy_client.get_product_by_domain(domain)

async def enhanced_risk_score_with_privacyspy(text: str, domain: str) -> tuple[float, Dict[str, Any]]:
    privacyspy_data = await get_privacyspy_data(domain)
    
    base_risk_score = 50.0
    
    enhanced_insights = {
        "data_source": "heuristic",
        "privacyspy_available": False,
        "privacyspy_score": None,
        "data_sensitivity": "medium",
        "user_control": "medium", 
        "transparency": "medium",
        "compliance": "medium",
        "key_concerns": [],
        "privacy_strengths": [],
        "attribution": "Privacy Radar analysis"
    }
    
    if privacyspy_data:
        enhanced_insights["privacyspy_available"] = True
        enhanced_insights["privacyspy_score"] = privacyspy_data.get("score", 0)
        
        privacyspy_risk = privacyspy_client.convert_privacyspy_score_to_risk(
            privacyspy_data.get("score", 0)
        )
        
        extracted_insights = privacyspy_client.extract_enhanced_insights(privacyspy_data)
        enhanced_insights.update(extracted_insights)
        
        base_risk_score = privacyspy_risk
        enhanced_insights["data_source"] = "privacyspy"
        enhanced_insights["attribution"] = PRIVACYSPY_ATTRIBUTION
        
        from .scoring import risk_score
        heuristic_score = risk_score(text)
        
        if not privacyspy_data:
            base_risk_score = heuristic_score
            enhanced_insights["data_source"] = "heuristic"
        else:
            base_risk_score = (privacyspy_risk * 0.7) + (heuristic_score * 0.3)
            enhanced_insights["data_source"] = "blended"
            enhanced_insights["heuristic_score"] = heuristic_score
    
    return base_risk_score, enhanced_insights