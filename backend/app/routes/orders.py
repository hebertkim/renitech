# app/routes/order.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.order import OrderCreate, Order, OrderStatus
from app.crud import order as crud_order

router = APIRouter(prefix="/orders", tags=["Orders"])

# =========================
# Criar pedido
# =========================
@router.post("/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        return crud_order.create_order(db, order.user_id, [item.dict() for item in order.items])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# =========================
# Listar pedidos
# =========================
@router.get("/", response_model=List[Order])
def list_orders(db: Session = Depends(get_db)):
    return crud_order.list_orders(db)

# =========================
# Obter pedido por ID
# =========================
@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = crud_order.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

# =========================
# Atualizar status
# =========================
@router.patch("/{order_id}/status", response_model=Order)
def update_status(order_id: str, status: OrderStatus, db: Session = Depends(get_db)):
    try:
        return crud_order.update_order_status(db, order_id, status)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# =========================
# Deletar pedido
# =========================
@router.delete("/{order_id}")
def delete_order(order_id: str, db: Session = Depends(get_db)):
    try:
        crud_order.delete_order(db, order_id)
        return {"detail": "Pedido deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
