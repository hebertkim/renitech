from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db

# =========================
# 3.6 - Saúde Financeira
# =========================
from app.services.financial_health import calculate_financial_health

# =========================
# 3.7 - Recomendações Inteligentes
# =========================
from app.services.recommendation_service import RecommendationService
from app.schemas.recommendation import RecommendationsResponse

# =========================
# 3.8 - Score Financeiro
# =========================
from app.services.financial_score_service import FinancialScoreService
from app.schemas.financial_score import FinancialScoreResponse

# =========================
# 3.9 - Previsão Financeira
# =========================
from app.services.forecast_service import ForecastService
from app.schemas.dashboard import ForecastResponse

# =========================
# 3.10 - Simulador de Cenários
# =========================
from app.schemas.scenario import ScenarioSimulationRequest, ScenarioSimulationResponse
from app.services.scenario_simulation_service import ScenarioSimulationService

# =========================
# 3.11 - Risco de Endividamento Futuro
# =========================
from app.services.debt_risk_service import DebtRiskService
from app.schemas.debt_risk import DebtRiskResponse

# =========================
# 3.12 - Planejador Automático de Metas
# =========================
from app.services.financial_goals_service import FinancialGoalsService
from app.schemas.financial_goals import FinancialGoalsResponse

# =========================
# 3.13 - Otimizador Automático de Orçamento
# =========================
from app.services.budget_optimizer_service import BudgetOptimizerService
from app.schemas.budget_optimizer import BudgetOptimizerResponse

# =========================
# 3.14 - Análise de Risco Financeiro
# =========================
from app.services.risk_analysis_service import RiskAnalysisService
from app.schemas.risk_analysis import RiskAnalysisResponse

# =========================
# 3.15 a 3.19 - Alertas Inteligentes Proativos
# =========================
from app.services.alert_engine_service import AlertEngineService
from app.schemas.alert_response import AlertsResponse

# =========================
# 3.20 - Alertas de Metas por Categoria
# =========================
from app.services.category_goal_alert_service import CategoryGoalAlertService

# =========================
# 3.21 - Análise de Oportunidades Financeiras
# =========================
from app.services.opportunity_analysis_service import OpportunityAnalysisService
from app.schemas.opportunity_analysis import OpportunityAnalysisResponse


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

# =========================
# 3.6 - Saúde Financeira
# =========================
@router.get("/health")
def financial_health(db: Session = Depends(get_db)):
    return calculate_financial_health(db)

# =========================
# 3.7 - Recomendações Inteligentes
# =========================
@router.get("/recommendations", response_model=RecommendationsResponse)
def get_recommendations(db: Session = Depends(get_db)):
    return RecommendationService.generate(db)

# =========================
# 3.8 - Score Financeiro
# =========================
@router.get("/score", response_model=FinancialScoreResponse)
def get_financial_score(db: Session = Depends(get_db)):
    return FinancialScoreService.calculate(db)

# =========================
# 3.9 - Previsão Financeira
# =========================
@router.get("/forecast", response_model=ForecastResponse)
def get_forecast(
    months: int = Query(6, ge=1, le=24, description="Quantidade de meses para previsão"),
    db: Session = Depends(get_db)
):
    return ForecastService.generate_forecast(db, months)

# =========================
# 3.10 - Simulador de Cenários (What-if)
# =========================
@router.post("/simulate", response_model=ScenarioSimulationResponse)
def simulate_scenario(
    payload: ScenarioSimulationRequest,
    db: Session = Depends(get_db)
):
    return ScenarioSimulationService.simulate(db, payload)

# =========================
# 3.11 - Risco de Endividamento Futuro
# =========================
@router.get("/debt-risk", response_model=DebtRiskResponse)
def get_debt_risk(
    months: int = Query(6, ge=3, le=24, description="Janela de meses para análise de risco"),
    db: Session = Depends(get_db)
):
    return DebtRiskService.analyze(db, months)

# =========================
# 3.12 - Planejador Automático de Metas
# =========================
@router.get("/goals", response_model=FinancialGoalsResponse)
def get_financial_goals(db: Session = Depends(get_db)):
    return FinancialGoalsService.generate(db)

# =========================
# 3.13 - Otimizador Automático de Orçamento
# =========================
@router.get("/optimize-budget", response_model=BudgetOptimizerResponse)
def optimize_budget(db: Session = Depends(get_db)):
    return BudgetOptimizerService.optimize(db)

# =========================
# 3.14 - Análise de Risco Financeiro (global ou por período)
# =========================
@router.get("/risk", response_model=RiskAnalysisResponse)
def analyze_risk(
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=2000, le=2100),
    db: Session = Depends(get_db)
):
    return RiskAnalysisService.analyze(db, month, year)

# =========================
# 3.15 a 3.19 - Alertas Inteligentes Proativos
# =========================
@router.get("/alerts", response_model=AlertsResponse)
def get_alerts(db: Session = Depends(get_db)):
    """
    Retorna todos os alertas proativos, incluindo:
    - Saúde financeira (3.6)
    - Score financeiro (3.8)
    - Risco de endividamento (3.11)
    - Previsão financeira (3.9)
    - Otimização de orçamento (3.13)
    - Alertas por categoria (3.18)
    - Alertas por metas de categoria (3.19)
    """
    return AlertEngineService.generate(db)

# =========================
# 3.20 - Alertas de Metas por Categoria
# =========================
@router.get("/goals-alerts", response_model=AlertsResponse)
def get_goals_alerts(db: Session = Depends(get_db)):
    alerts = CategoryGoalAlertService.analyze(db)

    if not alerts:
        summary = "Todas as metas estão dentro do esperado. Nenhum alerta crítico no momento."
    else:
        criticals = len([a for a in alerts if a["level"] == "critical"])
        warnings = len([a for a in alerts if a["level"] == "warning"])
        summary = f"{criticals} alertas críticos e {warnings} alertas de atenção detectados."

    return {
        "alerts": alerts,
        "summary": summary
    }

# =========================
# 3.21 - Oportunidades Financeiras
# =========================
@router.get("/opportunities", response_model=OpportunityAnalysisResponse)
def get_opportunities(db: Session = Depends(get_db)):
    """
    Retorna oportunidades de otimização financeira:
    - Ajustes de gastos
    - Economia por categoria
    - Sugestões baseadas no score e saúde financeira
    """
    return OpportunityAnalysisService.analyze(db)
