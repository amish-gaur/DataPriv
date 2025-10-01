from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SummarizeRequest(BaseModel):
    domain: str
    candidate_urls: List[str] = []

class Summary(BaseModel):
    data_collected: List[str] = []
    purposes: List[str] = []
    sharing: Optional[str] = None
    retention: Optional[str] = None
    user_rights: Optional[str] = None

class SummarizeResponse(BaseModel):
    domain: str
    source_url: str
    summary: Summary
    risk_score: float
    enhanced_insights: Optional[Dict[str, Any]] = None
