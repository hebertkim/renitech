from sqlalchemy.orm import Session
from datetime import date
from app.models.expense import Expense
from app.models.income import Income
from app.models.category import Category
from app.models.alert_history import AlertHistory

from app.services.intelligence_service import calculate_score  # Score do usuário

def get_dashboard_data(db: Session, user_id: int):
    # 🔹 Total receitas
    total_income = db.query(Income).filter(Income.user_id == user_id).with_entities(
        func.coalesce(func.sum(Income.valor), 0)
    ).scalar() or 0

    # 🔹 Total despesas
    total_expense = db.query(Expense).filter(Expense.user_id == user_id).with_entities(
        func.coalesce(func.sum(Expense.valor), 0)
    ).scalar() or 0

    # 🔹 Saldo
    balance = total_income - total_expense

    # 🔹 Score
    score = calculate_score(db, user_id)

    # 🔹 Gastos por categoria
    category_expenses = []
    categories = db.query(Category).all()
    for cat in categories:
        expenses = db.query(Expense).filter(
            Expense.user_id == user_id, Expense.category_id == cat.id
        ).all()
        if not expenses:
            continue
        total_cat = sum(e.valor for e in expenses)
        avg_cat = total_cat / len(expenses)
        category_expenses.append({
            "category_id": cat.id,
            "category_name": cat.name,
            "total": total_cat,
            "average": avg_cat
        })

    # 🔹 Alertas recentes
    alerts = db.query(AlertHistory).filter(AlertHistory.user_id == user_id).order_by(
        AlertHistory.id.desc()
    ).limit(10).all()
    alerts_data = []
    for a in alerts:
        alerts_data.append({
            "id": a.id,
            "title": a.title,
            "level": a.level,
            "message": a.message,
            "date": a.created_at.strftime("%Y-%m-%d")
        })

    return {
        "summary": {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "score": score
        },
        "category_expenses": category_expenses,
        "alerts": alerts_data
    }
