# app/crud/income.py
from sqlalchemy.orm import Session
from app.models.income import Income
from app.schemas.income import IncomeCreate, IncomeUpdate
from datetime import datetime
from decimal import Decimal

# =========================
# CREATE
# =========================
def create_income(db: Session, data: IncomeCreate, user_id: int, account_id: int):
    inc = Income(
        description=data.description.strip().capitalize(),
        amount=Decimal(data.amount),
        date=data.date,
        category_id=data.category_id,
        account_id=account_id,
        user_id=user_id
    )
    db.add(inc)
    db.commit()
    db.refresh(inc)
    return inc

# =========================
# LIST
# =========================
def list_incomes(db: Session, user_id: int):
    return db.query(Income).filter(Income.user_id == user_id).order_by(Income.date.desc()).all()

# =========================
# GET
# =========================
def get_income(db: Session, income_id: int, user_id: int):
    return db.query(Income).filter(Income.id == income_id, Income.user_id == user_id).first()

# =========================
# UPDATE
# =========================
def update_income(db: Session, income_id: int, data: IncomeUpdate, user_id: int, account_id: int):
    inc = get_income(db, income_id, user_id)
    if not inc:
        return None
    inc.description = data.description.strip().capitalize()
    inc.amount = Decimal(data.amount)
    inc.date = data.date
    inc.category_id = data.category_id
    inc.account_id = account_id
    inc.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(inc)
    return inc

# =========================
# DELETE
# =========================
def delete_income(db: Session, income_id: int, user_id: int):
    inc = get_income(db, income_id, user_id)
    if not inc:
        return None
    db.delete(inc)
    db.commit()
    return inc
