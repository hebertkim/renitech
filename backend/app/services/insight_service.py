from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date

from app.models.expense import Expense
from app.models.income import Income
from app.models.category import Category
from app.schemas.dashboard import InsightItem, InsightsResponse


class InsightService:

    @staticmethod
    def generate_insights(db: Session) -> InsightsResponse:
        insights = []

        today = date.today()
        current_year = today.year
        current_month = today.month

        # =========================
        # Função mês anterior
        # =========================
        def prev_month(year, month):
            if month == 1:
                return year - 1, 12
            return year, month - 1

        py, pm = prev_month(current_year, current_month)

        # =========================
        # 1. Gastos mês atual vs anterior
        # =========================

        current_expense = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
            extract("year", Expense.date) == current_year,
            extract("month", Expense.date) == current_month,
        ).scalar() or 0

        prev_expense = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
            extract("year", Expense.date) == py,
            extract("month", Expense.date) == pm,
        ).scalar() or 0

        if prev_expense > 0:
            diff = (float(current_expense) - float(prev_expense)) / float(prev_expense) * 100

            if diff > 20:
                insights.append(InsightItem(
                    type="danger",
                    message=f"⚠️ Seus gastos aumentaram {diff:.1f}% em relação ao mês passado.",
                ))
            elif diff < -20:
                insights.append(InsightItem(
                    type="success",
                    message=f"✅ Seus gastos caíram {-diff:.1f}% em relação ao mês passado.",
                ))

        # =========================
        # 2. Tendência de saldo (3 meses)
        # =========================

        balances = []

        y, m = current_year, current_month
        for _ in range(3):
            income = db.query(func.coalesce(func.sum(Income.amount), 0)).filter(
                extract("year", Income.date) == y,
                extract("month", Income.date) == m,
            ).scalar() or 0

            expense = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
                extract("year", Expense.date) == y,
                extract("month", Expense.date) == m,
            ).scalar() or 0

            balances.append(float(income) - float(expense))

            if m == 1:
                y -= 1
                m = 12
            else:
                m -= 1

        if len(balances) == 3:
            if balances[0] < balances[1] < balances[2]:
                insights.append(InsightItem(
                    type="success",
                    message="📈 Seu saldo está em tendência de crescimento nos últimos meses.",
                ))
            elif balances[0] > balances[1] > balances[2]:
                insights.append(InsightItem(
                    type="warning",
                    message="📉 Seu saldo está em tendência de queda nos últimos meses.",
                ))

        # =========================
        # 3. Categoria fora do padrão
        # =========================

        categories = db.query(Category).filter(Category.type == "expense").all()

        for cat in categories:
            avg = db.query(func.avg(Expense.amount)).filter(
                Expense.category_id == cat.id
            ).scalar()

            if not avg:
                continue

            current = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
                Expense.category_id == cat.id,
                extract("year", Expense.date) == current_year,
                extract("month", Expense.date) == current_month,
            ).scalar() or 0

            if float(current) > float(avg) * 1.5:
                insights.append(InsightItem(
                    type="warning",
                    message=f"💸 Você está gastando muito acima do normal na categoria '{cat.name}'.",
                ))

        # =========================
        # 4. Receita caindo
        # =========================

        current_income = db.query(func.coalesce(func.sum(Income.amount), 0)).filter(
            extract("year", Income.date) == current_year,
            extract("month", Income.date) == current_month,
        ).scalar() or 0

        prev_income = db.query(func.coalesce(func.sum(Income.amount), 0)).filter(
            extract("year", Income.date) == py,
            extract("month", Income.date) == pm,
        ).scalar() or 0

        if prev_income > 0 and float(current_income) < float(prev_income) * 0.8:
            insights.append(InsightItem(
                type="danger",
                message="🚨 Sua receita caiu significativamente em relação ao mês passado.",
            ))

        # =========================
        # Fallback
        # =========================

        if not insights:
            insights.append(InsightItem(
                type="info",
                message="ℹ️ Nenhum insight crítico detectado no momento. Sua vida financeira está estável.",
            ))

        return InsightsResponse(insights=insights)
