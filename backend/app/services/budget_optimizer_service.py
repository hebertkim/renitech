from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.expense import Expense
from app.models.category import Category
from app.schemas.budget_optimizer import (
    BudgetOptimizerResponse,
    BudgetCategorySuggestion
)


class BudgetOptimizerService:

    @staticmethod
    def optimize(db: Session) -> BudgetOptimizerResponse:
        # =========================
        # Total gasto por categoria
        # =========================
        rows = (
            db.query(
                Category.id,
                Category.name,
                func.coalesce(func.sum(Expense.amount), 0).label("total")
            )
            .outerjoin(Expense, Expense.category_id == Category.id)
            .filter(Category.type == "expense")
            .group_by(Category.id, Category.name)
            .all()
        )

        if not rows:
            return BudgetOptimizerResponse(
                total_current_expense=0,
                total_suggested_expense=0,
                estimated_saving=0,
                suggestions=[]
            )

        data = [(r.name, float(r.total)) for r in rows]
        total_expense = sum(v for _, v in data)

        # =========================
        # Heurística de otimização
        # =========================
        # Nenhuma categoria deve ultrapassar 30% do total
        # Categorias muito pequenas podem aumentar até 10%
        # =========================
        max_ratio = 0.30
        min_ratio_increase = 0.05  # até 5% do total pode aumentar

        suggestions = []
        new_total = 0

        for name, value in data:
            ratio = value / total_expense if total_expense > 0 else 0

            if ratio > max_ratio:
                suggested = total_expense * max_ratio
                action = "reduce"
            elif ratio < min_ratio_increase:
                suggested = value * 1.1
                action = "increase"
            else:
                suggested = value
                action = "keep"

            suggested = round(suggested, 2)
            new_total += suggested

            suggestions.append(
                BudgetCategorySuggestion(
                    category_name=name,
                    current=round(value, 2),
                    suggested=suggested,
                    difference=round(suggested - value, 2),
                    action=action
                )
            )

        return BudgetOptimizerResponse(
            total_current_expense=round(total_expense, 2),
            total_suggested_expense=round(new_total, 2),
            estimated_saving=round(total_expense - new_total, 2),
            suggestions=suggestions
        )
