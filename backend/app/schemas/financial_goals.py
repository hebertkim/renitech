from pydantic import BaseModel
from typing import List

class FinancialGoalItem(BaseModel):
    title: str
    description: str
    target_value: float
    deadline_months: int
    priority: str  # low | medium | high | critical

class FinancialGoalsResponse(BaseModel):
    current_status: str
    goals: List[FinancialGoalItem]
