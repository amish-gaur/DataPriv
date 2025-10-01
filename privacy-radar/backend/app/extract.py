import httpx, re
from bs4 import BeautifulSoup
from readability import Document

CAND_PAT = re.compile(r"(privacy|policy|terms|cookie)", re.I)

def pick_best_url(domain: str, candidates: list[str]) -> str | None:
    uniq = list(dict.fromkeys(candidates))
    if not uniq:
        # fallback guess
        return f"https://{domain}/privacy"  # may 404; backend will handle
    ranked = sorted(uniq, key=lambda u: (
        0 if re.search(r"privacy|policy", u, re.I) else 1,
        0 if re.search(r"terms", u, re.I) else 1,
        len(u)
    ))
    return ranked[0]

async def fetch_text(url: str) -> tuple[str, str]:
    async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
        r = await client.get(url)
        r.raise_for_status()
        html = r.text
        doc = Document(html)
        readable_html = doc.summary()
        soup = BeautifulSoup(readable_html, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return (html, text)
