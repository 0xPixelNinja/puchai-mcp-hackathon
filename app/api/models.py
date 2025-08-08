from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    preferences: Optional[dict] = None

class Recommendation(BaseModel):
    product_name: str
    recommendation_reason: str
    confidence_score: float
    pros: List[str]
    cons: List[str]
    source_summary: str

class RecommendationResponse(BaseModel):
    query: str
    recommendations: List[Recommendation]
    summary: str

