from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from app.database import get_db
from app.models.expense import Expense, PaymentMethodEnum, ReconciliationStatusEnum
from app.models.account import Account
from app.models.category import Category
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, Expense as ExpenseSchema
from app.dependencies import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# =========================
# Helpers
# =========================
def get_default_account(db: Session) -> Account:
    acc = db.query(Account).filter(Account.name == "Default").first()
    if not acc:
        acc = Account(name="Default", balance=0)
        db.add(acc)
        db.commit()
        db.refresh(acc)
    return acc

def validate_expense(db: Session, data: ExpenseCreate | ExpenseUpdate):
    if data.category_id:
        cat = db.query(Category).filter(Category.id == data.category_id).first()
        if not cat or cat.type != "expense":
            raise HTTPException(status_code=400, detail="Categoria inválida para despesas")

# =========================
# CRUD Routes
# =========================
@router.post("/", response_model=ExpenseSchema)
def create_new_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    validate_expense(db, data)
    default_account = get_default_account(db)

    exp = Expense(
        description=data.description.strip().capitalize(),
        amount=Decimal(data.amount),
        currency=data.currency,
        date=data.date,
        due_date=data.due_date,
        paid=data.paid,
        payment_method=data.payment_method,
        invoice_number=data.invoice_number,
        supplier=data.supplier,
        fiscal_class=data.fiscal_class,
        tax_amount=data.tax_amount,
        recurring=data.recurring,
        recurrence_rule=data.recurrence_rule,
        attachment=data.attachment,
        reconciliation_status=data.reconciliation_status,
        reconciliation_date=data.reconciliation_date,
        notes=data.notes,
        ai_risk_flag=data.ai_risk_flag,
        ai_category_suggestion=data.ai_category_suggestion,
        category_id=data.category_id,
        account_id=default_account.id,
        user_id=current_user.id
    )

    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

@router.get("/", response_model=List[ExpenseSchema])
def list_expenses(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    min_amount: Optional[Decimal] = Query(None),
    max_amount: Optional[Decimal] = Query(None),
    category_id: Optional[int] = Query(None),
    text: Optional[str] = Query(None),
    order: str = Query("date_desc"),
    limit: int = Query(100, le=500),
    offset: int = Query(0)
):
    q = db.query(Expense).filter(Expense.user_id == current_user.id)

    if date_from:
        q = q.filter(Expense.date >= date_from)
    if date_to:
        q = q.filter(Expense.date <= date_to)
    if min_amount is not None:
        q = q.filter(Expense.amount >= min_amount)
    if max_amount is not None:
        q = q.filter(Expense.amount <= max_amount)
    if category_id:
        q = q.filter(Expense.category_id == category_id)
    if text:
        q = q.filter(Expense.description.ilike(f"%{text}%"))

    if order == "date_asc":
        q = q.order_by(Expense.date.asc())
    elif order == "amount_asc":
        q = q.order_by(Expense.amount.asc())
    elif order == "amount_desc":
        q = q.order_by(Expense.amount.desc())
    else:
        q = q.order_by(Expense.date.desc())

    return q.offset(offset).limit(limit).all()

@router.get("/{id}", response_model=ExpenseSchema)
def get_single_expense(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    obj = db.query(Expense).filter(Expense.id == id, Expense.user_id == current_user.id).first()
    if not obj:
        raise HTTPEx
