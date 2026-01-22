# app/crud/expense.py
from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from datetime import datetime
from decimal import Decimal

# =========================
# CREATE
# =========================
def create_expense(db: Session, data: ExpenseCreate, user_id: int, account_id: int):
    exp = Expense(
        description=data.description.strip().capitalize(),
        amount=Decimal(data.amount),
        date=data.date,
        category_id=data.category_id,
        account_id=account_id,
        user_id=user_id
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

# =========================
# LIST
# =========================
def list_expenses(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).order_by(Expense.date.desc()).all()

# =========================
# GET
# =========================
def get_expense(db: Session, expense_id: int, user_id: int):
    return db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()

# =========================
# UPDATE
# =========================
def update_expense(db: Session, expense_id: int, data: ExpenseUpdate, user_id: int, account_id: int):
    exp = get_expense(db, expense_id, user_id)
    if not exp:
        return None
    exp.description = data.description.strip().capitalize()
    exp.amount = Decimal(data.amount)
    exp.date = data.date
    exp.category_id = data.category_id
    exp.account_id = account_id
    exp.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(exp)
    return exp

# =========================
# DELETE
# =========================
def delete_expense(db: Session, expense_id: int, user_id: int):
    exp = get_expense(db, expense_id, user_id)
    if not exp:
        return None
    db.delete(exp)
    db.commit()
    return exp
