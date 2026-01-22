from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date

from app.models.expense import Expense
from app.models.income import Income
from app.services.anomaly_service import AnomalyService
from app.schemas.financial_score import FinancialScoreResponse, FinancialScoreDetails


class FinancialScoreService:

    @staticmethod
    def calculate(db: Session) -> FinancialScoreResponse:
        today = date.today()
        year = today.year

        # =========================
        # Totais do ano
        # =========================
        total_income = db.query(func.coalesce(func.sum(Income.amount), 0)).filter(
            extract("year", Income.date) == year
        ).scalar() or 0

        total_expense = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
            extract("year", Expense.date) == year
        ).scalar() or 0

        total_income = float(total_income)
        total_expense = float(total_expense)

        if total_income <= 0:
            return FinancialScoreResponse(
                score=0,
                level="critical",
                details=FinancialScoreDetails(
                    saving_rate=0,
                    expense_ratio=1,
                    trend="stable",
                    anomalies=0
                )
            )

        # =========================
        # Métricas base
        # =========================
        saving_rate = max(0, (total_income - total_expense) / total_income) * 100
        expense_ratio = total_expense / total_income

        # =========================
        # Tendência de 3 meses
        # =========================
        balances = []
        y, m = today.year, today.month
        for _ in range(3):
            inc = db.query(func.coalesce(func.sum(Income.amount), 0)).filter(
                extract("year", Income.date) == y,
                extract("month", Income.date) == m,
            ).scalar() or 0

            exp = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
                extract("year", Expense.date) == y,
                extract("month", Expense.date) == m,
            ).scalar() or 0

            balances.append(float(inc) - float(exp))

            if m == 1:
                y -= 1
                m = 12
            else:
                m -= 1

        trend = "stable"
        if len(balances) == 3:
            if balances[0] > balances[1] > balances[2]:
                trend = "up"
            elif balances[0] < balances[1] < balances[2]:
                trend = "down"

        # =========================
        # Anomalias
        # =========================
        anomalies = len(AnomalyService.detect_expense_anomalies(db)) + len(
            AnomalyService.detect_income_anomalies(db)
        )

        # =========================
        # Cálculo do score
        # =========================
        score = 100

        # Penaliza gasto alto
        if expense_ratio > 0.9:
            score -= 30
        elif expense_ratio > 0.8:
            score -= 20
        elif expense_ratio > 0.7:
            score -= 10

        # Bonifica poupança
        if saving_rate > 30:
            score += 10
        elif saving_rate > 20:
            score += 5

        # Tendência
        if trend == "down":
            score -= 10
        elif trend == "up":
            score += 5

        # Anomalias
        score -= anomalies * 5

        # Limites
        score = max(0, min(100, score))

        # =========================
        # Nível textual
        # =========================
        if score < 30:
            level = "critical"
        elif score < 50:
            level = "bad"
        elif score < 70:
            level = "ok"
        elif score < 85:
            level = "good"
        else:
            level = "excellent"

        return FinancialScoreResponse(
            score=score,
            level=level,
            details=FinancialScoreDetails(
                saving_rate=round(saving_rate, 2),
                expense_ratio=round(expense_ratio, 2),
                trend=trend,
                anomalies=anomalies
            )
        )
