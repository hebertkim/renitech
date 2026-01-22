from sqlalchemy.orm import Session

from app.services.financial_health import calculate_financial_health
from app.services.financial_score_service import FinancialScoreService
from app.services.forecast_service import ForecastService
from app.schemas.financial_goals import FinancialGoalsResponse, FinancialGoalItem


class FinancialGoalsService:

    @staticmethod
    def generate(db: Session) -> FinancialGoalsResponse:
        health = calculate_financial_health(db)
        score = FinancialScoreService.calculate(db)
        forecast = ForecastService.generate_forecast(db, 6)

        goals = []

        # =========================
        # 1) Reserva de emergência
        # =========================
        avg_expense = 0
        if forecast.projections:
            avg_expense = sum(p.expense for p in forecast.projections) / len(forecast.projections)

        emergency_target = round(avg_expense * 6, 2) if avg_expense > 0 else 5000

        goals.append(FinancialGoalItem(
            title="Criar reserva de emergência",
            description="Guardar o equivalente a 6 meses do seu custo de vida.",
            target_value=emergency_target,
            deadline_months=12,
            priority="critical" if health["status"] in ["bad", "critical"] else "high"
        ))

        # =========================
        # 2) Sair do saldo negativo
        # =========================
        worst_balance = min(p.balance for p in forecast.projections) if forecast.projections else 0

        if worst_balance < 0:
            goals.append(FinancialGoalItem(
                title="Eliminar saldo negativo",
                description="Ajustar despesas e aumentar receitas para sair do prejuízo mensal.",
                target_value=abs(round(worst_balance, 2)),
                deadline_months=6,
                priority="critical"
            ))

        # =========================
        # 3) Melhorar score financeiro
        # =========================
        if score.score < 70:
            goals.append(FinancialGoalItem(
                title="Melhorar score financeiro",
                description="Organizar finanças para atingir um score acima de 70.",
                target_value=70,
                deadline_months=9,
                priority="high" if score.score < 50 else "medium"
            ))

        # =========================
        # 4) Crescimento patrimonial
        # =========================
        goals.append(FinancialGoalItem(
            title="Aumentar patrimônio líquido",
            description="Construir crescimento consistente de saldo positivo.",
            target_value=round(emergency_target * 0.3, 2),
            deadline_months=12,
            priority="medium"
        ))

        # =========================
        # Status geral
        # =========================
        if health["status"] in ["critical", "bad"]:
            status = "recovery"
        elif score.score < 60:
            status = "restructuring"
        else:
            status = "growth"

        return FinancialGoalsResponse(
            current_status=status,
            goals=goals
        )
