from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.expense import Expense
from app.models.category import Category


class CategoryAlertService:

    @staticmethod
    def analyze(db: Session, months: int = 1):
        """
        Analisa os gastos por categoria e gera alertas caso estejam acima da média.
        """
        alerts = []

        # =========================
        # Calcular data limite
        # =========================
        from datetime import date, timedelta
        today = date.today()
        start_date = today - timedelta(days=30 * months)

        # =========================
        # Buscar total gasto por categoria
        # =========================
        rows = (
            db.query(
                Category.id,
                Category.name,
                func.coalesce(func.sum(Expense.amount), 0).label("total")
            )
            .outerjoin(Expense, (Expense.category_id == Category.id) & (Expense.date >= start_date))
            .filter(Category.type == "expense")
            .group_by(Category.id, Category.name)
            .all()
        )

        if not rows:
            return alerts

        totals = [float(r.total) for r in rows]
        avg = sum(totals) / len(totals) if totals else 0

        # =========================
        # Gerar alertas
        # =========================
        for r in rows:
            category = r.name
            total = float(r.total)

            # Acima da média
            if total > avg * 1.8:
                alerts.append({
                    "level": "warning",
                    "title": f"Gastos elevados em {category}",
                    "message": f"Seus gastos em '{category}' estão muito acima da média das outras categorias."
                })

            # Crítico: consumindo fatia absurda
            if total > avg * 3:
                alerts.append({
                    "level": "critical",
                    "title": f"Gastos críticos em {category}",
                    "message": f"A categoria '{category}' está comprometendo seriamente seu orçamento."
                })

        return alerts
