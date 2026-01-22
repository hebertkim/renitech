from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date
from typing import List

from app.database import get_db
from app.models.expense import Expense
from app.models.income import Income
from app.models.category import Category
from app.models.account import Account
from app.models.alert_history import AlertHistory

from app.schemas.dashboard import (
    DashboardSummary,
    CategorySummary,
    MonthlyEvolutionItem,
    MonthlyEvolutionResponse,
    AccountSummary,
    TopCategoryItem,
    AnomalyItem,
    TrendItem,
    TrendsResponse,
    InsightItem,
    InsightsResponse,
    ForecastResponse,
)

from app.services.anomaly_service import AnomalyService
from app.services.insight_service import InsightService
from app.services.forecast_service import ForecastService
from app.services.alert_service import detect_expense_anomalies  # 🔹 integração 3.23

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# =========================
# Dashboard Summary
# =========================
@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=2000, le=2100),
):
    expense_q = db.query(Expense)
    income_q = db.query(Income)

    if month and year:
        expense_q = expense_q.filter(
            extract("month", Expense.date) == month,
            extract("year", Expense.date) == year,
        )
        income_q = income_q.filter(
            extract("month", Income.date) == month,
            extract("year", Income.date) == year,
        )

    total_expense = float(expense_q.with_entities(func.coalesce(func.sum(Expense.amount), 0)).scalar() or 0)
    total_income = float(income_q.with_entities(func.coalesce(func.sum(Income.amount), 0)).scalar() or 0)

    balance = total_income - total_expense

    expenses_by_category_q = (
        db.query(Category.id, Category.name, func.coalesce(func.sum(Expense.amount), 0))
        .join(Expense, Expense.category_id == Category.id)
        .filter(Category.type == "expense")
        .group_by(Category.id, Category.name)
    )

    if month and year:
        expenses_by_category_q = expenses_by_category_q.filter(
            extract("month", Expense.date) == month,
            extract("year", Expense.date) == year,
        )

    expenses_by_category = [
        CategorySummary(category_id=r[0], category_name=r[1], total=float(r[2]))
        for r in expenses_by_category_q.all()
    ]

    incomes_by_category_q = (
        db.query(Category.id, Category.name, func.coalesce(func.sum(Income.amount), 0))
        .join(Income, Income.category_id == Category.id)
        .filter(Category.type == "income")
        .group_by(Category.id, Category.name)
    )

    if month and year:
        incomes_by_category_q = incomes_by_category_q.filter(
            extract("month", Income.date) == month,
            extract("year", Income.date) == year,
        )

    incomes_by_category = [
        CategorySummary(category_id=r[0], category_name=r[1], total=float(r[2]))
        for r in incomes_by_category_q.all()
    ]

    return DashboardSummary(
        total_income=round(total_income, 2),
        total_expense=round(total_expense, 2),
        balance=round(balance, 2),
        expenses_by_category=expenses_by_category,
        incomes_by_category=incomes_by_category,
    )

# =========================
# Evolução Mensal
# =========================
@router.get("/monthly-evolution", response_model=MonthlyEvolutionResponse)
def get_monthly_evolution(
    db: Session = Depends(get_db),
    months: int = Query(12, ge=1, le=60)
):
    today = date.today()
    start_date = date(today.year, today.month, 1)

    for _ in range(months - 1):
        if start_date.month == 1:
            start_date = date(start_date.year - 1, 12, 1)
        else:
            start_date = date(start_date.year, start_date.month - 1, 1)

    incomes_raw = (
        db.query(
            extract("year", Income.date).label("year"),
            extract("month", Income.date).label("month"),
            func.coalesce(func.sum(Income.amount), 0).label("total"),
        )
        .filter(Income.date >= start_date)
        .group_by("year", "month")
        .all()
    )

    expenses_raw = (
        db.query(
            extract("year", Expense.date).label("year"),
            extract("month", Expense.date).label("month"),
            func.coalesce(func.sum(Expense.amount), 0).label("total"),
        )
        .filter(Expense.date >= start_date)
        .group_by("year", "month")
        .all()
    )

    incomes_map = {(int(r.year), int(r.month)): float(r.total) for r in incomes_raw}
    expenses_map = {(int(r.year), int(r.month)): float(r.total) for r in expenses_raw}

    result = []
    current = start_date

    for _ in range(months):
        y, m = current.year, current.month
        income = incomes_map.get((y, m), 0)
        expense = expenses_map.get((y, m), 0)

        result.append(MonthlyEvolutionItem(
            year=y,
            month=m,
            income=round(income, 2),
            expense=round(expense, 2),
            balance=round(income - expense, 2),
        ))

        if current.month == 12:
            current = date(current.year + 1, 1, 1)
        else:
            current = date(current.year, current.month + 1, 1)

    return MonthlyEvolutionResponse(data=result)

# =========================
# Por conta
# =========================
@router.get("/by-account", response_model=List[AccountSummary])
def get_dashboard_by_account(db: Session = Depends(get_db)):
    accounts = db.query(Account).all()
    result = []

    for acc in accounts:
        income = sum(float(i.amount) for i in acc.incomes)
        expense = sum(float(e.amount) for e in acc.expenses)

        result.append(AccountSummary(
            account_id=acc.id,
            account_name=acc.name,
            income=round(income, 2),
            expense=round(expense, 2),
            balance=round(income - expense, 2),
        ))

    return result

# =========================
# Top categorias
# =========================
@router.get("/top-expense-categories", response_model=List[TopCategoryItem])
def get_top_expense_categories(db: Session = Depends(get_db), limit: int = 5):
    q = (
        db.query(Category.id, Category.name, func.sum(Expense.amount))
        .join(Expense)
        .filter(Category.type == "expense")
        .group_by(Category.id, Category.name)
        .order_by(func.sum(Expense.amount).desc())
        .limit(limit)
    )
    return [TopCategoryItem(category_id=r[0], category_name=r[1], total=float(r[2])) for r in q.all()]

@router.get("/top-income-categories", response_model=List[TopCategoryItem])
def get_top_income_categories(db: Session = Depends(get_db), limit: int = 5):
    q = (
        db.query(Category.id, Category.name, func.sum(Income.amount))
        .join(Income)
        .filter(Category.type == "income")
        .group_by(Category.id, Category.name)
        .order_by(func.sum(Income.amount).desc())
        .limit(limit)
    )
    return [TopCategoryItem(category_id=r[0], category_name=r[1], total=float(r[2])) for r in q.all()]

# =========================
# Anomalias (3.23 integrado)
# =========================
@router.get("/anomalies", response_model=List[AnomalyItem])
def get_anomalies(db: Session = Depends(get_db)):
    anomalies = AnomalyService.detect_expense_anomalies(db) + AnomalyService.detect_income_anomalies(db)
    # 🔹 integração alertas despesas fora do padrão
    extra_alerts = detect_expense_anomalies(db, user_id=1)  # ajustar conforme auth futura
    for a in extra_alerts:
        anomalies.append(AnomalyItem(
            id=a.id,
            type=a.tipo,
            description=a.mensagem,
            amount=a.valor,
            date=str(a.data),
            category_name=None,
            account_name=None
        ))
    return anomalies

# =========================
# Tendências
# =========================
@router.get("/trends", response_model=TrendsResponse)
def get_trends(db: Session = Depends(get_db)):
    return TrendItem.build(db)

# =========================
# INSIGHTS (3.4)
# =========================
@router.get("/insights", response_model=InsightsResponse)
def get_insights(db: Session = Depends(get_db)):
    return InsightsResponse(insights=InsightService.generate_insights(db))

# =========================
# FORECAST (3.5)
# =========================
@router.get("/forecast", response_model=ForecastResponse)
def get_forecast(
    db: Session = Depends(get_db),
    months: int = Query(6, ge=1, le=36)
):
    return ForecastService.generate_forecast(db, months)
