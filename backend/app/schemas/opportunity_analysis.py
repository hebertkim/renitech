from pydantic import BaseModel
from typing import List

class OpportunityItem(BaseModel):
    type: str
    title: str
    message: str

class OpportunityAnalysisResponse(BaseModel):
    opportunities: List[OpportunityItem]
    summary: str
