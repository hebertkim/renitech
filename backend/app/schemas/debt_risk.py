from pydantic import BaseModel
from typing import List

class DebtRiskResponse(BaseModel):
    risk_level: str  # low | medium | high | critical
    probability: float  # 0.0 - 1.0
    main_factors: List[str]
    recommendations: List[str]
