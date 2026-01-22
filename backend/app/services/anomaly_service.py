from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.expense import Expense
from app.models.income import Income
from app.schemas.dashboard import AnomalyItem


class AnomalyService:

    # =========================
    # Despesas anômalas
    # =========================
    @staticmethod
    def detect_expense_anomalies(db: Session):
        stats = db.query(
            func.avg(Expense.amount),
            func.stddev(Expense.amount)
        ).first()

        if not stats or not stats[0]:
            return []

        avg, std = float(stats[0]), float(stats[1] or 0)

        threshold = avg + (2 * std)

        anomalies = (
            db.query(Expense)
            .filter(Expense.amount > threshold)
            .all()
        )

        result = []

        for e in anomalies:
            result.append(
                AnomalyItem(
                    id=e.id,
                    type="expense",
                    description=e.description,
                    amount=float(e.amount),
                    date=str(e.date),
                    category_name=e.category.name if e.category else None,
                    account_name=e.account.name if e.account else None,
                )
            )

        return result

    # =========================
    # Receitas anômalas
    # =========================
    @staticmethod
    def detect_income_anomalies(db: Session):
        stats = db.query(
            func.avg(Income.amount),
            func.stddev(Income.amount)
        ).first()

        if not stats or not stats[0]:
            return []

        avg, std = float(stats[0]), float(stats[1] or 0)

        threshold = avg + (2 * std)

        anomalies = (
            db.query(Income)
            .filter(Income.amount > threshold)
            .all()
        )

        result = []

        for i in anomalies:
            result.append(
                AnomalyItem(
                    id=i.id,
                    type="income",
                    description=i.description,
                    amount=float(i.amount),
                    date=str(i.date),
                    category_name=i.category.name if i.category else None,
                    account_name=i.account.name if i.account else None,
                )
            )

        return result
