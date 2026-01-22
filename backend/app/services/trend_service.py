from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from datetime import date

from app.models.expense import Expense
from app.models.income import Income
from app.models.category import Category


class TrendService:

    @staticmethod
    def _get_last_months(months: int = 6):
        today = date.today()
        result = []
        y, m = today.year, today.month

        for _ in range(months):
            result.append((y, m))
            if m == 1:
                y -= 1
                m = 12
            else:
                m -= 1

        return list(reversed(result))

    @staticmethod
    def _calc_trend(values: list[float]):
        if len(values) < 2:
            return 0

        # tendência simples: diferença entre último e primeiro
        return values[-1] - values[0]

    # =============================
    # Tendência de despesas
    # =============================
    @staticmethod
    def expense_trends(db: Session, months: int = 6):
        timeline = TrendService._get_last_months(months)
        result = []

        categories = db.query(Category).filter(Category.type == "expense").all()

        for cat in categories:
            series = []

            for y, m in timeline:
                total = (
                    db.query(func.coalesce(func.sum(Expense.amount), 0))
                    .filter(
                        Expense.category_id == cat.id,
                        extract("year", Expense.date) == y,
                        extract("month", Expense.date) == m,
                    )
                    .scalar()
                )
                series.append(float(total or 0))

            trend = TrendService._calc_trend(series)

            if trend > 0:
                direction = "up"
            elif trend < 0:
                direction = "down"
            else:
                direction = "stable"

            projection = series[-1] + trend / max(1, len(series))

            result.append({
                "category_id": cat.id,
                "category_name": cat.name,
                "series": series,
                "trend": round(trend, 2),
                "direction": direction,
                "projection_next_month": round(projection, 2),
            })

        return result
