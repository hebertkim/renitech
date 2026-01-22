# app/routers/income.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal

from app.database import get_db
from app.models.account import Account
from app.models.category import Category
from app.schemas.income import IncomeCreate, IncomeUpdate, Income as IncomeSchema
from app.dependencies import get_current_user
from app.crud import income as crud_income

router = APIRouter(prefix="/incomes", tags=["Incomes"])

# =========================
# Helpers
# =========================
def get_default_account(db: Session) -> Account:
    """Retorna a conta Default, criando se não existir"""
    acc = db.query(Account).filter(Account.name == "Default").first()
    if not acc:
        acc = Account(name="Default", balance=0)
        db.add(acc)
        db.commit()
        db.refresh(acc)
    return acc

def validate_income_category(db: Session, category_id: Optional[int]):
    """Valida se a categoria existe e é do tipo 'income'"""
    if category_id:
        cat = db.query(Category).filter(Category.id == category_id).first()
        if not cat or getattr(cat, "type", None) != "income":
            raise HTTPException(status_code=400, detail="Categoria inválida para receitas")

# =========================
# CRUD Routes
# =========================
@router.post("/", response_model=IncomeSchema)
def create_income(
    data: IncomeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    validate_income_category(db, data.category_id)
    default_account = get_default_account(db)
    inc = crud_income.create_income(
        db=db,
        data=data,
        user_id=current_user.id,
        account_id=default_account.id
    )
    return inc

@router.get("/", response_model=List[IncomeSchema])
def list_incomes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    min_amount: Optional[Decimal] = Query(None),
    max_amount: Optional[Decimal] = Query(None),
    category_id: Optional[int] = Query(None),
    text: Optional[str] = Query(None),
    order: str = Query("date_desc"),
    limit: int = Query(100, le=500),
    offset: int = Query(0)
):
    q = db.query(crud_income.Income).filter(crud_income.Income.user_id == current_user.id)

    if date_from:
        q = q.filter(crud_income.Income.date >= date_from)
    if date_to:
        q = q.filter(crud_income.Income.date <= date_to)
    if min_amount is not None:
        q = q.filter(crud_income.Income.amount >= min_amount)
    if max_amount is not None:
        q = q.filter(crud_income.Income.amount <= max_amount)
    if category_id:
        q = q.filter(crud_income.Income.category_id == category_id)
    if text:
        q = q.filter(crud_income.Income.description.ilike(f"%{text}%"))

    if order == "date_asc":
        q = q.order_by(crud_income.Income.date.asc())
    elif order == "amount_asc":
        q = q.order_by(crud_income.Income.amount.asc())
    elif order == "amount_desc":
        q = q.order_by(crud_income.Income.amount.desc())
    else:
        q = q.order_by(crud_income.Income.date.desc())

    return q.offset(offset).limit(limit).all()

@router.get("/{id}", response_model=IncomeSchema)
def get_income(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    inc = crud_income.get_income(db, id, current_user.id)
    if not inc:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    return inc

@router.put("/{id}", response_model=IncomeSchema)
def update_income(
    id: int,
    data: IncomeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    validate_income_category(db, data.category_id)
    default_account = get_default_account(db)
    inc = crud_income.update_income(
        db, income_id=id, data=data, 
        user_id=current_user.id,
        account_id=default_account.id
    )
    if not inc:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    return inc

@router.delete("/{id}")
def delete_income(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    inc = crud_income.delete_income(db, income_id=id, user_id=current_user.id)
    if not inc:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    return {"detail": "Receita removida"}
