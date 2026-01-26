# app/routes/stock.py

from typing import List
from enum import Enum
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.stock import Stock, StockCreate
from app.crud import stock as crud
from app.models.user import User

# ✅ AUTH CENTRALIZADA
from app.dependencies import require_admin, require_staff

# ==============================
# Enum para movimento de estoque
# ==============================
class MovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"

# ==============================
# Router
# ==============================
router = APIRouter(prefix="/stocks", tags=["Stocks"])

# =========================
# ADICIONAR ESTOQUE (ADMIN)
# =========================
@router.post("/{product_id}/add", response_model=Stock)
def add_stock_route(
    product_id: str,
    stock_data: StockCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),  # 🔒 Só admin
):
    if stock_data.movement_type != MovementType.IN:
        raise HTTPException(
            status_code=400,
            detail="Use 'IN' movement_type for addition"
        )

    movement = crud.add_stock(
        db=db,
        product_id=product_id,
        quantity=stock_data.quantity
    )

    return Stock.from_orm(movement)


# =========================
# REMOVER ESTOQUE (ADMIN)
# =========================
@router.post("/{product_id}/remove", response_model=Stock)
def remove_stock_route(
    product_id: str,
    stock_data: StockCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),  # 🔒 Só admin
):
    if stock_data.movement_type != MovementType.OUT:
        raise HTTPException(
            status_code=400,
            detail="Use 'OUT' movement_type for removal"
        )

    movement = crud.remove_stock(
        db=db,
        product_id=product_id,
        quantity=stock_data.quantity
    )

    return Stock.from_orm(movement)


# =========================
# LISTAR MOVIMENTOS (STAFF)
# =========================
@router.get("/{product_id}/movements", response_model=List[Stock])
def list_stock_movements_route(
    product_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),  # 🔒 vendedor, admin, superadmin
):
    movements = crud.get_stock_movements(db=db, product_id=product_id)
    return [Stock.from_orm(m) for m in movements]
