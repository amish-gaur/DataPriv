import re

KEYWORDS = {
    "sell": 20, "third party": 12, "advertis": 10, "retain indefinitely": 10,
    "biometric": 18, "location": 10, "cookie": 6, "share": 8, "tracking": 8
}
SAFE = {
    "do not sell": -15, "no sale": -15, "data minimization": -8,
    "delete your data": -10, "opt-out": -8, "opt out": -8, "gdpr": -5, "ccpa": -5
}

def risk_score(text: str) -> float:
    t = text.lower()
    score = 0
    for k, w in KEYWORDS.items():
        score += len(re.findall(k, t)) * w
    for k, w in SAFE.items():
        score += len(re.findall(k, t)) * w
    return max(0.0, min(99.0, float(score)))
