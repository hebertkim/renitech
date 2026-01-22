from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date, timedelta

from app.models.expense import Expense
from app.models.income import Income
from app.schemas.recommendation import RecommendationItem, RecommendationsResponse

class RecommendationService:

    @staticmethod
    def generate(db: Session) -> RecommendationsResponse:
        recs = []

        # =========================
        # Total geral
        # =========================
        total_income = db.query(func.coalesce(func.sum(Income.amount), 0)).scalar() or 0
        total_expense = db.query(func.coalesce(func.sum(Expense.amount), 0)).scalar() or 0

        if total_expense > total_income:
            recs.append(RecommendationItem(
                level="danger",
                title="Gastos maiores que receitas",
                message="Você está gastando mais do que ganha no total acumulado. É urgente reduzir despesas."
            ))
        else:
            recs.append(RecommendationItem(
                level="success",
                title="Saldo positivo geral",
                message="Parabéns! No total, suas receitas são maiores que suas despesas."
            ))

        # =========================
        # Últimos 3 meses
        # =========================
        today = date.today()
        start_date = today - timedelta(days=90)

        income_3m = db.query(func.coalesce(func.sum(Income.amount), 0)).filter(Income.date >= start_date).scalar() or 0
        expense_3m = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(Expense.date >= start_date).scalar() or 0

        if expense_3m > income_3m:
            recs.append(RecommendationItem(
                level="warning",
                title="Prejuízo recente",
                message="Nos últimos 3 meses você gastou mais do que ganhou. Atenção ao seu ritmo financeiro."
            ))
        else:
            recs.append(RecommendationItem(
                level="success",
                title="Boa gestão recente",
                message="Nos últimos 3 meses você manteve saldo positivo. Continue assim."
            ))

        # =========================
        # Categoria dominante
        # =========================
        top_category = (
            db.query(Expense.category_id, func.sum(Expense.amount).label("total"))
            .group_by(Expense.category_id)
            .order_by(func.sum(Expense.amount).desc())
            .first()
        )

        if top_category:
            perc = (float(top_category.total) / float(total_expense)) * 100 if total_expense > 0 else 0

            if perc > 40:
                recs.append(RecommendationItem(
                    level="warning",
                    title="Gasto concentrado demais",
                    message="Uma única categoria representa mais de 40% dos seus gastos. Avalie se isso é saudável."
                ))

        # =========================
        # Nenhuma movimentação
        # =========================
        total_ops = db.query(Expense).count() + db.query(Income).count()

        if total_ops == 0:
            recs.append(RecommendationItem(
                level="info",
                title="Sem dados suficientes",
                message="Ainda não há movimentações suficientes para gerar recomendações inteligentes."
            ))

        return RecommendationsResponse(recommendations=recs)
