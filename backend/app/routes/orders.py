# app/routes/orders.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.order import (
    create_order,
    update_order_status,
    delete_order,
    list_orders,
    get_order
)
from app.schemas.order import OrderCreate, Order, OrderStatusUpdate
from app.database import get_db
from app.models.user import User
from app.security import get_current_user

# ==============================
# Router
# ==============================
router = APIRouter(prefix="/orders", tags=["Orders"])

# ==============================
# DEPENDÊNCIAS DE PERMISSÃO
# ==============================
def require_staff(user: User = Depends(get_current_user)):
    if user.role not in ["vendedor", "admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user

def require_admin(user: User = Depends(get_current_user)):
    if user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user

# ==============================
# Criar pedido (STAFF)
# ==============================
@router.post("/", response_model=Order)
def create_order_endpoint(
    order: OrderCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),
):
    return create_order(db=db, order=order)

# ==============================
# Atualizar status do pedido (STAFF)
# ==============================
@router.put("/{order_id}/status", response_model=Order)
def update_order_status_endpoint(
    order_id: str,
    status: OrderStatusUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),
):
    updated_order = update_order_status(
        db=db,
        order_id=order_id,
        status=status
    )
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

# ==============================
# Deletar pedido (ADMIN)
# ==============================
@router.delete("/{order_id}")
def delete_order_endpoint(
    order_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    deleted = delete_order(db=db, order_id=order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"success": True}

# ==============================
# Listar pedidos (STAFF)
# ==============================
@router.get("/", response_model=List[Order])
def list_orders_endpoint(
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),
):
    return list_orders(db=db)

# ==============================
# Obter pedido por ID (STAFF)
# ==============================
@router.get("/{order_id}", response_model=Order)
def get_order_endpoint(
    order_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),
):
    order = get_order(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
