import os, json
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .models import SummarizeRequest, SummarizeResponse, Summary
from .db import engine, init_db
from .extract import pick_best_url, fetch_text
from .scoring import risk_score, enhanced_risk_score
from .privacyspy import enhanced_risk_score_with_privacyspy

CORS_ORIGIN = os.getenv("CORS_ORIGIN", "*")
CACHE_TTL_DAYS = int(os.getenv("CACHE_TTL_DAYS", "14"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "").strip()

app = FastAPI(title="Privacy Radar API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CORS_ORIGIN, "http://localhost:3000"],
    allow_methods=["*"], allow_headers=["*"]
)

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "privacy-radar-api"}

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Privacy Radar API",
        "version": "1.0.0",
        "description": "Analyze website privacy policies and generate risk scores",
        "endpoints": {
            "POST /summarize": "Analyze a domain's privacy policy",
            "GET /health": "Health check",
            "GET /docs": "API documentation"
        }
    }

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(req: SummarizeRequest):
    # Validate input
    if not req.domain or not req.domain.strip():
        raise HTTPException(400, "Domain is required")
    
    # Clean domain
    domain = req.domain.strip().lower()
    if domain.startswith(('http://', 'https://')):
        from urllib.parse import urlparse
        domain = urlparse(domain).hostname or domain
    
    # try cache
    with engine.begin() as conn:
        cached = conn.execute(text(f"""
          SELECT domain, source_url, summary_json, risk_score,
                 (NOW() - updated_at) < INTERVAL '{CACHE_TTL_DAYS} days' as fresh
          FROM site_summary WHERE domain=:d
        """), {"d": domain}).fetchone()
    if cached and cached.fresh:
        return {
          "domain": cached.domain,
          "source_url": cached.source_url,
          "summary": cached.summary_json,
          "risk_score": float(cached.risk_score),
          "enhanced_insights": {
              "data_source": "cached",
              "privacyspy_available": False,
              "note": "Using cached analysis"
          }
        }

    try:
        src = pick_best_url(domain, req.candidate_urls)
        if not src:
            raise HTTPException(404, "No candidate policy URL found.")
        
        _, text_content = await fetch_text(src)
    except HTTPException:
        raise
    except Exception as e:
        # Graceful fallback: continue with empty text so clients still get a response
        print(f"Warning: Failed to fetch content for {domain}: {e}")
        text_content = ""
        src = f"https://{domain}/privacy"  # Fallback URL

    # If AI is available, get an AI summary; else heuristic
    ai_summary: dict | None = None
    ai_task = None
    if OPENAI_API_KEY or OLLAMA_HOST:
        ai_task = asyncio.create_task(ai_summarize(text_content))

    # Enhanced heuristic extraction
    t = text_content.lower()
    def has(k): return k in t

    # More comprehensive data collection detection
    data_collected = []
    data_keywords = [
        "email", "name", "phone", "location", "ip", "device", "cookie", "biometric", "payment",
        "address", "age", "gender", "birth", "ssn", "social security", "credit card", "bank",
        "financial", "health", "medical", "genetic", "dna", "sexual", "political", "religious",
        "browsing history", "search history", "purchase history", "device id", "fingerprint"
    ]
    for k in data_keywords:
        if has(k): data_collected.append(k)

    # More comprehensive purposes detection
    purposes = []
    purpose_keywords = [
        "ads", "advertising", "analytics", "personalization", "research", "improve services", 
        "security", "marketing", "profiling", "behavioral", "targeted", "recommendations",
        "customer service", "support", "legal", "compliance", "fraud prevention"
    ]
    for k in purpose_keywords:
        if has(k): purposes.append(k)

    # Enhanced sharing detection
    sharing = "limited/unspecified"
    if any(word in t for word in ["sell", "advertis", "share", "third party", "partner"]):
        if any(word in t for word in ["do not sell", "no sale", "no sharing"]):
            sharing = "not sold/shared"
        else:
            sharing = "sold/shared with advertisers/partners"
    elif any(word in t for word in ["no third party", "no sharing", "internal only"]):
        sharing = "not shared with third parties"

    # Enhanced retention detection
    retention = "unspecified"
    if "indefinite" in t or "permanent" in t:
        retention = "indefinite"
    elif "30 days" in t or "1 month" in t:
        retention = "30 days"
    elif "90 days" in t or "3 months" in t:
        retention = "90 days"
    elif "12 months" in t or "1 year" in t:
        retention = "12 months"
    elif "24 months" in t or "2 years" in t:
        retention = "24 months"
    elif "delete" in t and ("30" in t or "60" in t or "90" in t):
        retention = "automatic deletion"

    # Enhanced user rights detection
    rights = []
    rights_keywords = [
        "access", "delete", "portability", "opt-out", "opt out", "do not sell", "limit use",
        "correct", "update", "withdraw", "consent", "unsubscribe", "right to be forgotten",
        "data portability", "rectification", "erasure", "restriction", "objection"
    ]
    for k in rights_keywords:
        if has(k): rights.append(k)
    user_rights = ", ".join(sorted(set(rights))) or None

    # Use enhanced AI-powered risk scoring with PrivacySpy integration
    score, enhanced_insights = await enhanced_risk_score_with_privacyspy(text_content, domain)

    summary_obj = Summary(
        data_collected=sorted(set(data_collected)),
        purposes=purposes,
        sharing=sharing,
        retention=retention,
        user_rights=user_rights
    )

    if ai_task is not None:
        try:
            ai_summary = await asyncio.wait_for(ai_task, timeout=8)
        except Exception as e:
            print(f"Warning: AI summarization failed: {e}")
            ai_summary = None

    summary = (ai_summary or summary_obj.model_dump())

    # Store in database
    try:
        with engine.begin() as conn:
            conn.execute(text("""
              INSERT INTO site_summary(domain, source_url, summary_json, risk_score, updated_at)
              VALUES (:d, :u, CAST(:s AS JSONB), :r, NOW())
              ON CONFLICT (domain) DO UPDATE
                SET source_url=EXCLUDED.source_url,
                    summary_json=EXCLUDED.summary_json,
                    risk_score=EXCLUDED.risk_score,
                    updated_at=NOW()
            """), {"d": domain, "u": src, "s": json.dumps(summary), "r": float(score)})
    except Exception as e:
        print(f"Warning: Failed to store in database: {e}")

    # Add enhanced insights to the response
    response_data = {
        "domain": domain, 
        "source_url": src, 
        "summary": summary, 
        "risk_score": score,
        "enhanced_insights": enhanced_insights
    }
    
    return response_data


async def ai_summarize(text_content: str) -> dict | None:
    """Optional AI summarization using OpenAI or local Ollama.
    Returns Summary-like dict or None on failure.
    """
    content = text_content[:120000]
    if not content:
        return None

    prompt = (
        "Extract a concise privacy summary as strict JSON with keys: "
        "data_collected (string[]), purposes (string[]), sharing (string), retention (string), user_rights (string). "
        "Base only on the given policy text. If unknown, use empty array or 'unspecified'.\n\n"
        "Policy text:\n" + content
    )

    # Prefer OpenAI if key provided
    if OPENAI_API_KEY:
        try:
            import httpx
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
            body = {
                "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
                "temperature": 0.2,
            }
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.post("https://api.openai.com/v1/chat/completions", json=body, headers=headers)
                r.raise_for_status()
                data = r.json()
                message = data["choices"][0]["message"]["content"]
                return json.loads(message)
        except Exception:
            return None

    # Otherwise try Ollama
    if OLLAMA_HOST:
        try:
            import httpx
            model = os.getenv("OLLAMA_MODEL", "llama3.1")
            payload = {"model": model, "prompt": prompt, "stream": False}
            url = f"{OLLAMA_HOST.rstrip('/')}/api/generate"
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.post(url, json=payload)
                r.raise_for_status()
                data = r.json()
                out = data.get("response", "{}").strip()
                # try to locate json inside
                start = out.find("{")
                end = out.rfind("}")
                if start != -1 and end != -1:
                    return json.loads(out[start:end+1])
        except Exception:
            return None

    return None
