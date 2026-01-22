from sqlalchemy.orm import Session

from app.services.forecast_service import ForecastService
from app.schemas.scenario import ScenarioSimulationRequest, ScenarioSimulationResponse
from app.schemas.dashboard import ForecastItem


class ScenarioSimulationService:

    @staticmethod
    def simulate(db: Session, payload: ScenarioSimulationRequest) -> ScenarioSimulationResponse:
        # =========================
        # Cenário original
        # =========================
        original_forecast = ForecastService.generate_forecast(db, payload.months)

        # =========================
        # Aplicar modificadores
        # =========================
        income_multiplier = 1 + (payload.income_change_percent / 100)
        expense_multiplier = 1 + (payload.expense_change_percent / 100)

        simulated = []

        simulated_risk = "safe"

        for item in original_forecast.projections:
            new_income = item.income * income_multiplier
            new_expense = item.expense * expense_multiplier
            new_balance = new_income - new_expense

            if new_balance < 0:
                simulated_risk = "critical"
            elif new_balance < new_income * 0.1 and simulated_risk != "critical":
                simulated_risk = "warning"

            simulated.append(
                ForecastItem(
                    year=item.year,
                    month=item.month,
                    income=round(new_income, 2),
                    expense=round(new_expense, 2),
                    balance=round(new_balance, 2),
                )
            )

        return ScenarioSimulationResponse(
            original=original_forecast.projections,
            simulated=simulated,
            original_risk=original_forecast.risk_level,
            simulated_risk=simulated_risk
        )
