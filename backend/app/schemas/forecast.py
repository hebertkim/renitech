# app/schemas/forecast.py

from pydantic import BaseModel
from typing import List

class ForecastItem(BaseModel):
    year: int
    month: int
    predicted_income: float
    predicted_expense: float
    predicted_balance: float
    accumulated_balance: float

class ForecastResponse(BaseModel):
    start_balance: float
    projections: List[ForecastItem]
