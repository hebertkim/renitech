from sqlalchemy.orm import Session

from app.services.forecast_service import ForecastService
from app.services.financial_score_service import FinancialScoreService
from app.services.financial_health import calculate_financial_health
from app.schemas.debt_risk import DebtRiskResponse


class DebtRiskService:

    @staticmethod
    def analyze(db: Session, months: int = 6) -> DebtRiskResponse:
        # Obter previsões e scores
        forecast = ForecastService.generate_forecast(db, months)
        score = FinancialScoreService.calculate(db)
        health = calculate_financial_health(db)

        # Contagem de meses negativos e saldo mínimo
        negative_months = 0
        min_balance = None

        for p in forecast.projections:
            if p.balance < 0:
                negative_months += 1
            if min_balance is None or p.balance < min_balance:
                min_balance = p.balance

        factors = []
        recommendations = []

        # =========================
        # Heurísticas de risco
        # =========================
        risk_points = 0

        if negative_months >= 3:
            risk_points += 4
            factors.append("Múltiplos meses com saldo negativo na previsão")
            recommendations.append("Reduzir despesas fixas imediatamente")

        if min_balance is not None and min_balance < -1000:
            risk_points += 2
            factors.append("Previsão de déficit acumulado alto")
            recommendations.append("Criar plano de recuperação financeira")

        if score.score < 40:
            risk_points += 3
            factors.append("Score financeiro muito baixo")
            recommendations.append("Evitar novas dívidas e reorganizar orçamento")

        if health["status"].lower() in ["crítico", "critical", "bad"]:
            risk_points += 3
            factors.append("Saúde financeira comprometida")
            recommendations.append("Cortar gastos não essenciais")

        # =========================
        # Classificação do risco
        # =========================
        if risk_points >= 8:
            level = "critical"
            probability = 0.9
        elif risk_points >= 5:
            level = "high"
            probability = 0.7
        elif risk_points >= 3:
            level = "medium"
            probability = 0.4
        else:
            level = "low"
            probability = 0.15

        if not recommendations:
            recommendations.append("Manter controle financeiro atual")
            factors.append("Situação financeira estável")

        return DebtRiskResponse(
            risk_level=level,
            probability=round(probability, 2),
            main_factors=factors,
            recommendations=recommendations
        )
