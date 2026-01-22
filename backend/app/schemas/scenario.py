from pydantic import BaseModel
from typing import List
from app.schemas.dashboard import ForecastItem


class ScenarioSimulationRequest(BaseModel):
    income_change_percent: float = 0   # ex: 10 = +10%, -5 = -5%
    expense_change_percent: float = 0  # ex: -10 = reduzir 10%
    months: int = 6


class ScenarioSimulationResponse(BaseModel):
    original: List[ForecastItem]
    simulated: List[ForecastItem]
    original_risk: str
    simulated_risk: str
