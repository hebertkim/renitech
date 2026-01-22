from pydantic import BaseModel
from typing import List

class BudgetCategorySuggestion(BaseModel):
    category_name: str
    current: float
    suggested: float
    difference: float
    action: str  # reduce | keep | increase

class BudgetOptimizerResponse(BaseModel):
    total_current_expense: float
    total_suggested_expense: float
    estimated_saving: float
    suggestions: List[BudgetCategorySuggestion]
