from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.models.expense import Expense
from app.models.income import Income

from app.services.financial_health import calculate_financial_health
from app.services.financial_score_service import FinancialScoreService


class RiskAnalysisService:

    @staticmethod
    def analyze(db: Session, month: Optional[int] = None, year: Optional[int] = None):
        # =========================
        # Define escopo
        # =========================
        period_label = "global"

        expense_query = db.query(Expense)
        income_query = db.query(Income)

        if month and year:
            period_label = f"{month:02d}/{year}"

            expense_query = expense_query.filter(
                Expense.date.month == month,
                Expense.date.year == year
            )

            income_query = income_query.filter(
                Income.date.month == month,
                Income.date.year == year
            )

        expenses = expense_query.all()
        incomes = income_query.all()

        total_expenses = sum(e.amount for e in expenses)
        total_income = sum(i.amount for i in incomes)

        # =========================
        # Métricas base
        # =========================
        health = calculate_financial_health(db)
        score_data = FinancialScoreService.calculate(db)
        score = score_data.score

        savings_rate = 0
        if total_income > 0:
            savings_rate = (total_income - total_expenses) / total_income

        # =========================
        # Fatores de risco
        # =========================
        factors = []
        risk_points = 0

        # 1️⃣ Gastando mais do que ganha
        if total_expenses > total_income:
            factors.append({
                "name": "Déficit financeiro",
                "level": "high",
                "description": "Você está gastando mais do que ganha."
            })
            risk_points += 40

        # 2️⃣ Taxa de poupança baixa
        if savings_rate < 0.05:
            factors.append({
                "name": "Baixa capacidade de poupança",
                "level": "medium",
                "description": "Sua taxa de poupança está muito baixa."
            })
            risk_points += 20

        # 3️⃣ Score financeiro ruim
        if score < 50:
            factors.append({
                "name": "Score financeiro baixo",
                "level": "high",
                "description": "Seu score financeiro indica alto risco estrutural."
            })
            risk_points += 30
        elif score < 70:
            factors.append({
                "name": "Score financeiro moderado",
                "level": "medium",
                "description": "Seu score financeiro indica risco moderado."
            })
            risk_points += 15

        # 4️⃣ Saúde financeira ruim
        if health["status"] in ["critical", "bad"]:
            factors.append({
                "name": "Saúde financeira comprometida",
                "level": "high",
                "description": "Sua saúde financeira geral está em estado crítico."
            })
            risk_points += 30

        # =========================
        # Normaliza score de risco (0 a 100)
        # =========================
        risk_score = min(100, risk_points)

        # =========================
        # Classificação final
        # =========================
        if risk_score < 25:
            risk_level = "low"
        elif risk_score < 50:
            risk_level = "medium"
        elif risk_score < 75:
            risk_level = "high"
        else:
            risk_level = "critical"

        # =========================
        # Sumário textual
        # =========================
        if risk_level == "low":
            summary = "Seu risco financeiro está sob controle."
        elif risk_level == "medium":
            summary = "Seu risco financeiro exige atenção."
        elif risk_level == "high":
            summary = "Seu risco financeiro é alto. Mudanças são recomendadas."
        else:
            summary = "Seu risco financeiro é crítico. Ação imediata é necessária."

        return {
            "period": period_label,
            "risk_score": float(risk_score),
            "risk_level": risk_level,
            "factors": factors,
            "summary": summary
        }
