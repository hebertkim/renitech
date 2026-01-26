# app/routes/dashboard.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.dashboard import (
    DashboardResponse,
    DashboardStats,
    LowStockProduct
)
from app.crud.dashboard import get_dashboard_data
from app.models.user import User
from app.security import get_current_user

# ==============================
# Router
# ==============================
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# ==============================
# DEPENDÊNCIA DE PERMISSÃO
# ==============================
def require_admin(user: User = Depends(get_current_user)):
    if user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user

# ==============================
# Função do Dashboard (ADMIN)
# ==============================
@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    dashboard_data = get_dashboard_data(db)

    low_stock_products = [
        LowStockProduct(
            product_id=product.id,
            product_name=product.name,
            stock_quantity=product.stock_quantity
        )
        for product in dashboard_data["low_stock_products"]
    ]

    stats = DashboardStats(
        total_products=dashboard_data["total_products"],
        total_categories=dashboard_data["total_categories"],
        total_orders=dashboard_data["total_orders"],
        total_customers=dashboard_data["total_customers"],
        low_stock_products_count=len(low_stock_products),
    )

    return DashboardResponse(
        stats=stats,
        low_stock_products=low_stock_products
    )
