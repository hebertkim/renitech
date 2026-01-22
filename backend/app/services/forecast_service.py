from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date

from app.models.expense import Expense
from app.models.income import Income
from app.schemas.dashboard import ForecastItem, ForecastResponse


class ForecastService:

    @staticmethod
    def generate_forecast(db: Session, months: int = 6) -> ForecastResponse:
        today = date.today()

        def month_start(d: date):
            return date(d.year, d.month, 1)

        # =========================
        # Últimos 12 meses como base histórica
        # =========================
        history_months = []
        current = month_start(today)

        for _ in range(12):
            history_months.append(current)
            if current.month == 1:
                current = date(current.year - 1, 12, 1)
            else:
                current = date(current.year, current.month - 1, 1)

        history_months = list(reversed(history_months))

        # =========================
        # Buscar receitas agregadas por mês
        # =========================
        incomes_raw = (
            db.query(
                extract("year", Income.date).label("year"),
                extract("month", Income.date).label("month"),
                func.coalesce(func.sum(Income.amount), 0).label("total"),
            )
            .filter(Income.date >= history_months[0])
            .group_by("year", "month")
            .all()
        )

        # =========================
        # Buscar despesas agregadas por mês
        # =========================
        expenses_raw = (
            db.query(
                extract("year", Expense.date).label("year"),
                extract("month", Expense.date).label("month"),
                func.coalesce(func.sum(Expense.amount), 0).label("total"),
            )
            .filter(Expense.date >= history_months[0])
            .group_by("year", "month")
            .all()
        )

        incomes_map = {(int(r.year), int(r.month)): float(r.total) for r in incomes_raw}
        expenses_map = {(int(r.year), int(r.month)): float(r.total) for r in expenses_raw}

        income_series = []
        expense_series = []

        for d in history_months:
            y, m = d.year, d.month
            income_series.append(incomes_map.get((y, m), 0))
            expense_series.append(expenses_map.get((y, m), 0))

        # =========================
        # Médias históricas
        # =========================
        avg_income = sum(income_series) / len(income_series) if income_series else 0
        avg_expense = sum(expense_series) / len(expense_series) if expense_series else 0

        # =========================
        # Tendência simples (aceleração)
        # =========================
        def trend(series: list[float]):
            if len(series) < 6:
                return 0
            prev = sum(series[-6:-3]) / 3
            curr = sum(series[-3:]) / 3
            return (curr - prev) / 3

        income_trend = trend(income_series)
        expense_trend = trend(expense_series)

        # =========================
        # Projeção futura
        # =========================
        projections = []

        current_year = today.year
        current_month = today.month

        base_income = avg_income
        base_expense = avg_expense

        risk = "safe"

        for i in range(1, months + 1):
            m = current_month + i
            y = current_year + (m - 1) // 12
            m = ((m - 1) % 12) + 1

            proj_income = base_income + income_trend * i
            proj_expense = base_expense + expense_trend * i
            balance = proj_income - proj_expense

            # =========================
            # Determina nível de risco
            # =========================
            if balance < 0:
                risk = "critical"
            elif balance < proj_income * 0.1 and risk != "critical":
                risk = "warning"

            projections.append(
                ForecastItem(
                    year=y,
                    month=m,
                    income=round(proj_income, 2),
                    expense=round(proj_expense, 2),
                    balance=round(balance, 2),
                )
            )

        return ForecastResponse(
            projections=projections,
            risk_level=risk
        )
