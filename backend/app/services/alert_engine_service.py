from sqlalchemy.orm import Session

from app.services.financial_health import calculate_financial_health
from app.services.financial_score_service import FinancialScoreService
from app.services.debt_risk_service import DebtRiskService
from app.services.forecast_service import ForecastService
from app.services.budget_optimizer_service import BudgetOptimizerService

# 🔥 3.18 - Alertas por Categoria
from app.services.category_alert_service import CategoryAlertService

# 🔥 3.19 - Alertas por Metas de Categoria
from app.services.category_goal_alert_service import CategoryGoalAlertService


class AlertEngineService:
    """
    Motor de alertas do Finzia.
    Consolida todos os alertas financeiros e retorna lista detalhada + resumo.
    """

    @staticmethod
    def generate(db: Session):
        alerts = []

        # =========================
        # 3.6 - Saúde Financeira
        # =========================
        health = calculate_financial_health(db)

        if health["status"].lower() in ["crítico", "critical"]:
            alerts.append({
                "level": "critical",
                "title": "Saúde financeira crítica",
                "message": "Seu nível de gastos compromete seriamente sua estabilidade financeira."
            })
        elif health["status"].lower() in ["atenção", "warning"]:
            alerts.append({
                "level": "warning",
                "title": "Saúde financeira em risco",
                "message": "Seus gastos estão muito próximos ou acima da sua renda."
            })

        # =========================
        # 3.8 - Score Financeiro
        # =========================
        score = FinancialScoreService.calculate(db)

        if score.score < 40:
            alerts.append({
                "level": "critical",
                "title": "Score financeiro muito baixo",
                "message": "Seu perfil financeiro está em alto risco de colapso."
            })
        elif score.score < 65:
            alerts.append({
                "level": "warning",
                "title": "Score financeiro baixo",
                "message": "Sua situação financeira precisa de ajustes urgentes."
            })

        # =========================
        # 3.11 - Risco de Endividamento Futuro
        # =========================
        debt = DebtRiskService.analyze(db, months=6)

        if debt.risk_level in ["critical", "high"]:
            alerts.append({
                "level": "critical",
                "title": "Alto risco de endividamento",
                "message": "Você provavelmente entrará em déficit financeiro nos próximos meses."
            })
        elif debt.risk_level == "medium":
            alerts.append({
                "level": "warning",
                "title": "Risco moderado de endividamento",
                "message": "Se continuar nesse ritmo, seu saldo pode se tornar negativo."
            })

        # =========================
        # 3.9 - Previsão Financeira
        # =========================
        forecast = ForecastService.generate_forecast(db, months=6)

        if forecast.risk_level == "critical":
            alerts.append({
                "level": "critical",
                "title": "Previsão financeira crítica",
                "message": "Seu saldo projetado ficará negativo em breve."
            })
        elif forecast.risk_level == "warning":
            alerts.append({
                "level": "warning",
                "title": "Previsão financeira preocupante",
                "message": "Sua margem de segurança financeira está muito baixa."
            })

        # =========================
        # 3.13 - Otimização de Orçamento
        # =========================
        budget = BudgetOptimizerService.optimize(db)

        if budget.estimated_saving > 0:
            alerts.append({
                "level": "info",
                "title": "Oportunidade de otimização de orçamento",
                "message": f"Você pode economizar até R$ {budget.estimated_saving:.2f} por mês."
            })

        # =========================
        # 3.18 - Alertas por Categoria
        # =========================
        category_alerts = CategoryAlertService.analyze(db)
        alerts.extend(category_alerts)

        # =========================
        # 3.19 - Alertas por Metas de Categoria
        # =========================
        category_goal_alerts = CategoryGoalAlertService.analyze(db)
        alerts.extend(category_goal_alerts)

        # =========================
        # Resumo
        # =========================
        if not alerts:
            summary = "Sua situação financeira está estável. Nenhum alerta crítico no momento."
        else:
            criticals = len([a for a in alerts if a["level"] == "critical"])
            warnings = len([a for a in alerts if a["level"] == "warning"])
            infos = len([a for a in alerts if a["level"] == "info"])

            summary = (
                f"{criticals} alertas críticos, "
                f"{warnings} alertas de atenção e "
                f"{infos} alertas informativos detectados."
            )

        return {
            "alerts": alerts,
            "summary": summary
        }
