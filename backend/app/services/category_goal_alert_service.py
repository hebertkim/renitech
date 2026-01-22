from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.models.expense import Expense
from app.models.category_goal import CategoryGoal


class CategoryGoalAlertService:
    """
    Analisa as metas de gasto por categoria e gera alertas caso estejam próximas ou excedam os limites.
    """

    @staticmethod
    def analyze(db: Session):
        alerts = []

        today = date.today()
        start_month = date(today.year, today.month, 1)

        # =========================
        # Buscar todas as metas por categoria
        # =========================
        goals = db.query(CategoryGoal).all()

        for goal in goals:
            # Total gasto na categoria neste mês
            total_spent = (
                db.query(func.coalesce(func.sum(Expense.amount), 0))
                .filter(
                    Expense.category_id == goal.category_id,
                    Expense.date >= start_month
                )
                .scalar()
            )

            # Percentual do objetivo atingido
            percent = (total_spent / goal.target_amount) * 100 if goal.target_amount else 0

            # =========================
            # Alertas
            # =========================
            if percent >= 100:
                alerts.append({
                    "level": "critical",
                    "title": f"Meta excedida em {goal.category.name}",
                    "message": f"Você já gastou R$ {total_spent:.2f}, ultrapassando a meta de R$ {goal.target_amount:.2f}."
                })
            elif percent >= 85:
                alerts.append({
                    "level": "warning",
                    "title": f"Meta próxima de limite em {goal.category.name}",
                    "message": f"Você gastou R$ {total_spent:.2f}, atingindo {percent:.0f}% da meta de R$ {goal.target_amount:.2f}."
                })

        return alerts
