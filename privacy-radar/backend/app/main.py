import os, json
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .models import SummarizeRequest, SummarizeResponse, Summary
from .db import engine, init_db
from .extract import pick_best_url, fetch_text
from .scoring import risk_score

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

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(req: SummarizeRequest):
    # try cache
    with engine.begin() as conn:
        cached = conn.execute(text(f"""
          SELECT domain, source_url, summary_json, risk_score,
                 (NOW() - updated_at) < INTERVAL '{CACHE_TTL_DAYS} days' as fresh
          FROM site_summary WHERE domain=:d
        """), {"d": req.domain}).fetchone()
    if cached and cached.fresh:
        return {
          "domain": cached.domain,
          "source_url": cached.source_url,
          "summary": cached.summary_json,
          "risk_score": float(cached.risk_score)
        }

    src = pick_best_url(req.domain, req.candidate_urls)
    if not src:
        raise HTTPException(404, "No candidate policy URL found.")
    try:
        _, text_content = await fetch_text(src)
    except Exception:
        # Graceful fallback: continue with empty text so clients still get a response
        text_content = ""

    # If AI is available, get an AI summary; else heuristic
    ai_summary: dict | None = None
    ai_task = None
    if OPENAI_API_KEY or OLLAMA_HOST:
        ai_task = asyncio.create_task(ai_summarize(text_content))

    # heuristic extraction
    t = text_content.lower()
    def has(k): return k in t

    data_collected = []
    for k in ["email", "name", "phone", "location", "ip", "device", "cookie", "biometric", "payment"]:
        if has(k): data_collected.append(k)

    purposes = [k for k in ["ads","analytics","personalization","research","improve services","security"] if has(k)]
    sharing = "sold/shared with advertisers" if ("sell" in t or "advertis" in t or "share" in t) else "limited/unspecified"
    retention = "indefinite" if "indefinite" in t else ("30 days" if "30 days" in t else ("12 months" if "12 months" in t else "unspecified"))
    rights = []
    for k in ["access","delete","portability","opt-out","opt out","do not sell","limit use"]:
        if has(k): rights.append(k)
    user_rights = ", ".join(sorted(set(rights))) or None

    score = risk_score(text_content)

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
        except Exception:
            ai_summary = None

    summary = (ai_summary or summary_obj.model_dump())

    with engine.begin() as conn:
        conn.execute(text("""
          INSERT INTO site_summary(domain, source_url, summary_json, risk_score, updated_at)
          VALUES (:d, :u, CAST(:s AS JSONB), :r, NOW())
          ON CONFLICT (domain) DO UPDATE
            SET source_url=EXCLUDED.source_url,
                summary_json=EXCLUDED.summary_json,
                risk_score=EXCLUDED.risk_score,
                updated_at=NOW()
        """), {"d": req.domain, "u": src, "s": json.dumps(summary), "r": float(score)})

    return {"domain": req.domain, "source_url": src, "summary": summary, "risk_score": score}


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
