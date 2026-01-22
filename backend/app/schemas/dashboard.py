from pydantic import BaseModel
from typing import List, Optional

# =========================
# Summary
# =========================

class CategorySummary(BaseModel):
    category_id: Optional[int]
    category_name: Optional[str]
    total: float

class DashboardSummary(BaseModel):
    total_income: float
    total_expense: float
    balance: float
    expenses_by_category: List[CategorySummary]
    incomes_by_category: List[CategorySummary]

    model_config = {"from_attributes": True}

# =========================
# Evolução mensal
# =========================

class MonthlyEvolutionItem(BaseModel):
    year: int
    month: int
    income: float
    expense: float
    balance: float

class MonthlyEvolutionResponse(BaseModel):
    data: List[MonthlyEvolutionItem]

# =========================
# Por conta
# =========================

class AccountSummary(BaseModel):
    account_id: int
    account_name: str
    income: float
    expense: float
    balance: float

# =========================
# Top categorias
# =========================

class TopCategoryItem(BaseModel):
    category_id: int
    category_name: str
    total: float

# =========================
# Anomalias
# =========================

class AnomalyItem(BaseModel):
    id: int
    type: str  # income | expense
    description: str
    amount: float
    date: str
    category_name: Optional[str]
    account_name: Optional[str]

# =========================
# Tendências
# =========================

class TrendItem(BaseModel):
    metric: str
    current_avg: float
    previous_avg: float
    change_percent: float
    trend: str  # up | down | stable

    @staticmethod
    def build(db):
        # mantido para não quebrar o que já existe
        return TrendsResponse(trends=[])

class TrendsResponse(BaseModel):
    trends: List[TrendItem]

# =====================
# INSIGHTS (3.4)
# =====================

class InsightItem(BaseModel):
    type: str  # info | success | warning | danger
    message: str

class InsightsResponse(BaseModel):
    insights: List[InsightItem]

# =====================
# FORECAST (3.5)
# =====================

class ForecastItem(BaseModel):
    year: int
    month: int
    income: float
    expense: float
    balance: float

class ForecastResponse(BaseModel):
    projections: List[ForecastItem]
    risk_level: str  # safe | warning | critical
