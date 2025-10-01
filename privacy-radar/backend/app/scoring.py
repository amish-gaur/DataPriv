import re
import os
import json
import asyncio
import httpx

KEYWORDS = {
    "sell": 20, "third party": 12, "advertis": 10, "retain indefinitely": 10,
    "biometric": 18, "location": 10, "cookie": 6, "share": 8, "tracking": 8,
    "personal information": 8, "data collection": 6, "user data": 6,
    "marketing": 5, "profiling": 12, "behavioral": 10, "surveillance": 15,
    "monitoring": 8, "analytics": 4, "personalized": 6, "targeted": 8,
    "cross-site": 10, "fingerprint": 12, "device id": 8, "ip address": 4,
    "browsing history": 8, "search history": 8, "purchase history": 8,
    "financial information": 12, "credit card": 15, "bank account": 15,
    "social security": 20, "ssn": 20, "tax id": 15, "passport": 15,
    "driver license": 15, "government id": 15, "health information": 18,
    "medical": 15, "genetic": 20, "dna": 20, "mental health": 15,
    "sexual orientation": 18, "political": 12, "religious": 12,
    "union membership": 15, "criminal": 15, "arrest": 15, "conviction": 15
}

SAFE = {
    "do not sell": -15, "no sale": -15, "data minimization": -8,
    "delete your data": -10, "opt-out": -8, "opt out": -8, "gdpr": -5, "ccpa": -5,
    "privacy by design": -10, "data protection": -5, "consent": -3,
    "transparent": -3, "user control": -5, "data portability": -5,
    "right to be forgotten": -8, "anonymize": -5, "pseudonymize": -3,
    "encrypt": -3, "secure": -2, "privacy first": -8, "user privacy": -5,
    "data subject rights": -5, "withdraw consent": -5, "data retention": -3,
    "limited retention": -5, "automatic deletion": -8, "data deletion": -5
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "").strip()

async def ai_risk_score(text: str) -> float:
    if not OPENAI_API_KEY and not OLLAMA_HOST:
        return None
    
    try:
        if OPENAI_API_KEY:
            import openai
            client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
            
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Analyze this privacy policy and provide a risk score from 0-99 where 0 is very low risk (privacy-friendly) and 99 is very high risk (privacy-concerning). Consider data collection, sharing, retention, user rights, and transparency. Respond with only a number."},
                    {"role": "user", "content": f"Privacy policy text:\n\n{text[:3000]}"}
                ],
                temperature=0.1
            )
            
            score_text = response.choices[0].message.content.strip()
            score = float(re.findall(r'\d+', score_text)[0])
            return max(0.0, min(99.0, score))
            
        elif OLLAMA_HOST:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{OLLAMA_HOST}/api/generate",
                    json={
                        "model": "llama2",
                        "prompt": f"Analyze this privacy policy and provide a risk score from 0-99 where 0 is very low risk (privacy-friendly) and 99 is very high risk (privacy-concerning). Consider data collection, sharing, retention, user rights, and transparency. Respond with only a number.\n\nPrivacy policy:\n{text[:3000]}",
                        "stream": False
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    score_text = result.get("response", "").strip()
                    score = float(re.findall(r'\d+', score_text)[0])
                    return max(0.0, min(99.0, score))
                    
    except Exception as e:
        print(f"AI scoring error: {e}")
        return None
    
    return None

def risk_score(text: str) -> float:
    text_lower = text.lower()
    score = 0.0
    
    for keyword, weight in KEYWORDS.items():
        if keyword in text_lower:
            count = text_lower.count(keyword)
            score += weight * count
    
    for keyword, weight in SAFE.items():
        if keyword in text_lower:
            count = text_lower.count(keyword)
            score += weight * count
    
    return max(0.0, min(99.0, float(score)))

async def enhanced_risk_score(text: str) -> float:
    if OPENAI_API_KEY or OLLAMA_HOST:
        ai_score = await ai_risk_score(text)
        if ai_score is not None:
            return ai_score
    return risk_score(text)