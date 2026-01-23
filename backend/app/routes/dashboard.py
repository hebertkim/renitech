# app/routes/dashboard.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.dashboard import DashboardResponse
from app.crud.dashboard import get_dashboard_data

# ==============================
# Router
# ==============================
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# =========================
# Função do Dashboard
# =========================
@router.get("/", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    dashboard_data = get_dashboard_data(db)  # Chama a função que busca os dados do banco
    low_stock_products = [
        LowStockProduct(
            product_id=product.id,
            product_name=product.name,
            stock_quantity=product.stock_quantity
        )
        for product in dashboard_data["low_stock_products"]
    ]

    return DashboardResponse(
        stats=DashboardStats(
            total_products=dashboard_data["total_products"],
            total_categories=dashboard_data["total_categories"],
            total_orders=dashboard_data["total_orders"],
            total_customers=dashboard_data["total_customers"],
            low_stock_products=len(low_stock_products),  # Número de produtos com estoque baixo
        ),
        low_stock_products=low_stock_products
    )
