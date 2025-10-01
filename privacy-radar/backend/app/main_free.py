import os
import json
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import SummarizeRequest, SummarizeResponse, Summary
from .extract import pick_best_url, fetch_text
from .scoring import risk_score, enhanced_risk_score
from .privacyspy import enhanced_risk_score_with_privacyspy

CORS_ORIGIN = os.getenv("CORS_ORIGIN", "*")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "").strip()

app = FastAPI(title="Privacy Radar API (Free Version)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CORS_ORIGIN, "http://localhost:3000"],
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "privacy-radar-api-free"}


@app.get("/")
async def root():
    return {
        "message": "Privacy Radar API (Free Version)",
        "version": "1.0.0",
        "endpoints": {
            "POST /summarize": "Analyze privacy policy",
            "GET /health": "Health check",
            "GET /docs": "API documentation"
        }
    }

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    if not req.domain or not req.domain.strip():
        raise HTTPException(400, "Domain is required")
    
    domain = req.domain.strip().lower()
    if domain.startswith("www."):
        domain = domain[4:]
    
    print(f"Analyzing domain: {domain}")
    
    candidate_urls = req.candidate_urls or []
    
    if not candidate_urls:
        candidate_urls = [
            f"https://{domain}/privacy",
            f"https://{domain}/privacy-policy",
            f"https://{domain}/terms",
            f"https://{domain}/terms-of-service",
            f"https://www.{domain}/privacy",
            f"https://www.{domain}/privacy-policy"
        ]
    
    src = pick_best_url(domain, candidate_urls)
    if not src:
        raise HTTPException(404, f"No privacy policy found for {domain}")
    
    print(f"Fetching text from: {src}")
    html_content, text_content = await fetch_text(src)
    if not text_content or len(text_content.strip()) < 100:
        # Try alternative URLs if the first one failed
        alternative_urls = [
            f"https://{domain}/terms",
            f"https://{domain}/legal",
            f"https://{domain}/data-policy",
            f"https://www.{domain}/terms",
            f"https://www.{domain}/legal"
        ]
        
        for alt_url in alternative_urls:
            print(f"Trying alternative URL: {alt_url}")
            html_content, text_content = await fetch_text(alt_url)
            if text_content and len(text_content.strip()) >= 100:
                src = alt_url
                break
        
        if not text_content or len(text_content.strip()) < 100:
            # Return a default analysis for sites without privacy policies
            return {
                "domain": domain,
                "source_url": "No privacy policy found",
                "summary": {
                    "data_collected": [],
                    "purposes": [],
                    "sharing": "Not specified - no privacy policy found",
                    "retention": "Not specified - no privacy policy found", 
                    "user_rights": "Not specified - no privacy policy found"
                },
                "risk_score": 75.0,  # High risk due to lack of transparency
                "enhanced_insights": {
                    "data_source": "no_policy",
                    "privacyspy_available": False,
                    "privacyspy_score": None,
                    "data_sensitivity": "unknown",
                    "user_control": "unknown",
                    "transparency": "low",
                    "compliance": "unknown",
                    "key_concerns": ["No privacy policy found", "Lack of transparency"],
                    "privacy_strengths": []
                }
            }
    
    print(f"Extracted {len(text_content)} characters of text")
    
    data_collected = []
    purposes = []
    sharing = None
    retention = None
    user_rights = None
    
    text_lower = text_content.lower()
    
    data_keywords = [
        "name", "email", "address", "phone", "location", "ip", "device", "browser",
        "cookie", "personal", "demographic", "financial", "health", "biometric",
        "behavioral", "preference", "purchase", "browsing", "search", "social"
    ]
    
    purpose_keywords = [
        "advertising", "marketing", "personalization", "analytics", "security",
        "support", "legal", "research", "improvement", "communication"
    ]
    
    sharing_keywords = [
        "third party", "partner", "advertiser", "vendor", "service provider",
        "affiliate", "subsidiary", "sold", "shared", "disclosed"
    ]
    
    retention_keywords = [
        "retain", "store", "keep", "delete", "remove", "purge", "archive",
        "permanent", "temporary", "duration", "period"
    ]
    
    rights_keywords = [
        "access", "delete", "correct", "update", "opt out", "opt-out",
        "withdraw", "consent", "portability", "restrict", "object"
    ]
    
    def has(keywords):
        return any(keyword in text_lower for keyword in keywords)
    
    for keyword in data_keywords:
        if has([keyword]):
            data_collected.append(keyword)
    
    for keyword in purpose_keywords:
        if has([keyword]):
            purposes.append(keyword)
    
    if has(sharing_keywords):
        if has(["not sold", "not shared", "not disclosed"]):
            sharing = "not sold/shared"
        elif has(["sold", "shared with advertisers", "shared with partners"]):
            sharing = "sold/shared with advertisers/partners"
        else:
            sharing = "limited/unspecified"
    else:
        sharing = "limited/unspecified"
    
    if has(retention_keywords):
        if has(["automatic deletion", "auto delete", "automatically remove"]):
            retention = "automatic deletion"
        elif has(["permanent", "indefinite", "forever"]):
            retention = "permanent"
        else:
            retention = "unspecified"
    else:
        retention = "unspecified"
    
    rights = []
    for k in rights_keywords:
        if has([k]): rights.append(k)
    user_rights = ", ".join(sorted(set(rights))) or None

    score, enhanced_insights = await enhanced_risk_score_with_privacyspy(text_content, domain)

    summary_obj = Summary(
        data_collected=sorted(set(data_collected)),
        purposes=purposes,
        sharing=sharing,
        retention=retention,
        user_rights=user_rights
    )

    ai_task = None
    if OPENAI_API_KEY or OLLAMA_HOST:
        ai_task = asyncio.create_task(ai_summarize(text_content))

    ai_summary = None
    if ai_task is not None:
        try:
            ai_summary = await asyncio.wait_for(ai_task, timeout=8)
        except Exception as e:
            print(f"Warning: AI summarization failed: {e}")
            ai_summary = None

    summary = (ai_summary or summary_obj.model_dump())

    response_data = {
        "domain": domain, 
        "source_url": src, 
        "summary": summary, 
        "risk_score": score,
        "enhanced_insights": enhanced_insights
    }
    
    
    return response_data


async def ai_summarize(text_content: str) -> dict | None:
    try:
        if OPENAI_API_KEY:
            import openai
            client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
            
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract privacy policy information in JSON format with fields: data_collected (list), purposes (list), sharing (string), retention (string), user_rights (string). Be concise and accurate."},
                    {"role": "user", "content": f"Analyze this privacy policy:\n\n{text_content[:4000]}"}
                ],
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            return json.loads(content.strip())
            
        elif OLLAMA_HOST:
            import httpx
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{OLLAMA_HOST}/api/generate",
                    json={
                        "model": "llama2",
                        "prompt": f"Extract privacy policy information in JSON format with fields: data_collected (list), purposes (list), sharing (string), retention (string), user_rights (string). Be concise and accurate.\n\nPrivacy policy:\n{text_content[:4000]}",
                        "stream": False
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result.get("response", "")
                    
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0]
                    elif "{" in content and "}" in content:
                        start = content.find("{")
                        end = content.rfind("}") + 1
                        content = content[start:end]
                    
                    return json.loads(content.strip())
                    
    except Exception as e:
        print(f"AI summarization error: {e}")
        return None
    
    return None