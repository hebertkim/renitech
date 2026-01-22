from sqlalchemy.orm import Session
from datetime import date
from app.models.expense import Expense
from app.models.alert import Alert

THRESHOLD_PERCENT = 20  # 20% acima da média

def detect_expense_anomalies(db: Session, user_id: int):
    alerts = []

    # Pegar todas as categorias usadas pelo usuário
    categories = db.query(Expense.category_id).filter(Expense.user_id == user_id).distinct()

    for cat in categories:
        # Pegar todas as despesas da categoria
        expenses = db.query(Expense).filter(
            Expense.user_id == user_id,
            Expense.category_id == cat[0]
        ).all()

        if not expenses:
            continue

        # Calcula média histórica usando o campo correto 'amount'
        avg = sum(e.amount for e in expenses) / len(expenses)

        # Verifica últimas despesas do dia
        today_expenses = [e for e in expenses if e.date == date.today()]

        for e in today_expenses:
            if e.amount > avg * (1 + THRESHOLD_PERCENT / 100):
                alert = Alert(
                    user_id=user_id,
                    category_id=cat[0],
                    tipo="despesa",
                    mensagem=f"Despesa acima do padrão na categoria {cat[0]}",
                    valor=e.amount,
                    threshold=THRESHOLD_PERCENT,
                    data=e.date
                )
                db.add(alert)
                alerts.append(alert)

    db.commit()
    return alerts
