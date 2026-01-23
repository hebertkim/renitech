# app/routes/stock.py
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.stock import Stock, StockCreate
from app.crud import stock as crud

# ==============================
# Router
# ==============================
router = APIRouter(prefix="/stocks", tags=["Stocks"])

# =========================
# Adicionar entrada de estoque
# =========================
@router.post("/{product_id}/add", response_model=Stock)
def add_stock_route(
    product_id: str,
    stock_data: StockCreate,
    db: Session = Depends(get_db)
):
    if stock_data.movement_type != "IN":
        raise HTTPException(status_code=400, detail="Use 'OUT' movement_type for removal")

    movement = crud.add_stock(
        db=db,
        product_id=product_id,
        quantity=stock_data.quantity
    )
    return movement

# =========================
# Remover estoque (saída)
# =========================
@router.post("/{product_id}/remove", response_model=Stock)
def remove_stock_route(
    product_id: str,
    stock_data: StockCreate,
    db: Session = Depends(get_db)
):
    if stock_data.movement_type != "OUT":
        raise HTTPException(status_code=400, detail="Use 'IN' movement_type for addition")

    movement = crud.remove_stock(
        db=db,
        product_id=product_id,
        quantity=stock_data.quantity
    )
    return movement

# =========================
# Listar movimentos de estoque
# =========================
@router.get("/{product_id}/movements", response_model=List[Stock])
def list_stock_movements_route(
    product_id: str,
    db: Session = Depends(get_db)
):
    movements = crud.get_stock_movements(db=db, product_id=product_id)
    return movements
