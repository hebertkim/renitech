from sqlalchemy.orm import Session
from datetime import date
from app.models.expense import Expense
from app.models.category import Category
from app.services.financial_health import calculate_financial_health
from app.services.budget_optimizer_service import BudgetOptimizerService
from app.services.financial_score_service import FinancialScoreService

class OpportunityAnalysisService:

    @staticmethod
    def analyze(db: Session):
        today = date.today()
        start_month = date(today.year, today.month, 1)

        opportunities = []

        # =========================
        # Avaliar saúde financeira
        # =========================
        health = calculate_financial_health(db)
        if health["status"] != "ok":
            opportunities.append({
                "type": "financial_health",
                "title": "Ajuste de gastos necessário",
                "message": "Sua saúde financeira não está ótima. Avalie reduzir gastos desnecessários."
            })

        # =========================
        # Avaliar orçamento
        # =========================
        budget = BudgetOptimizerService.optimize(db)
        if budget.reduction_needed > 0:
            opportunities.append({
                "type": "budget_optimization",
                "title": "Oportunidade de economia",
                "message": f"Você pode economizar até R$ {budget.reduction_needed:.2f} neste mês ajustando seus gastos."
            })

        # =========================
        # Avaliar categorias com maior impacto
        # =========================
        categories = db.query(Category).all()
        for cat in categories:
            total_spent = sum(e.amount for e in cat.expenses if e.date >= start_month)
            if total_spent > 0 and total_spent / (budget.total_income or 1) > 0.3:
                opportunities.append({
                    "type": "category_high_impact",
                    "title": f"Gastos altos em {cat.name}",
                    "message": f"A categoria {cat.name} consome {total_spent:.2f}, considere reduzir gastos."
                })

        # =========================
        # Avaliar score financeiro
        # =========================
        score = FinancialScoreService.calculate(db)
        if score.score < 65:
            opportunities.append({
                "type": "financial_score",
                "title": "Score financeiro baixo",
                "message": "Seu score financeiro indica que ajustes podem melhorar sua estabilidade."
            })

        return {
            "opportunities": opportunities,
            "summary": f"{len(opportunities)} oportunidades encontradas"
        }
