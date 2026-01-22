from pydantic import BaseModel
from typing import Optional, List


class RiskFactor(BaseModel):
    name: str
    level: str  # low | medium | high
    description: str


class RiskAnalysisResponse(BaseModel):
    period: Optional[str]  # "global" ou "01/2026"
    risk_score: float      # 0 a 100
    risk_level: str        # low | medium | high | critical
    factors: List[RiskFactor]
    summary: str
