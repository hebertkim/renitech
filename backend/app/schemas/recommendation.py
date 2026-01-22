from pydantic import BaseModel
from typing import List

class RecommendationItem(BaseModel):
    level: str  # info | warning | danger | success
    title: str
    message: str

class RecommendationsResponse(BaseModel):
    recommendations: List[RecommendationItem]
