from pydantic import BaseModel

class FinancialScoreDetails(BaseModel):
    saving_rate: float       # % do quanto sobra da renda
    expense_ratio: float     # despesas / receitas
    trend: str               # up | down | stable
    anomalies: int           # quantidade de anomalias

class FinancialScoreResponse(BaseModel):
    score: int               # 0 a 100
    level: str               # critical | bad | ok | good | excellent
    details: FinancialScoreDetails
