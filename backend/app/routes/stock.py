from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.stock import Stock, StockCreate
from app import crud, schemas
from app.database import get_db

router = APIRouter()

# Adicionar estoque (entrada)
@router.post("/stock/{product_id}/add", response_model=schemas.Stock)
def add_stock(product_id: str, quantity: float, db: Session = Depends(get_db)):
    return crud.add_stock(db=db, product_id=product_id, quantity=quantity)

# Remover estoque (saída)
@router.post("/stock/{product_id}/remove", response_model=schemas.Stock)
def remove_stock(product_id: str, quantity: float, db: Session = Depends(get_db)):
    return crud.remove_stock(db=db, product_id=product_id, quantity=quantity)

# Listar movimentos de estoque
@router.get("/stock/{product_id}/movements", response_model=List[schemas.Stock])
def list_stock_movements(product_id: str, db: Session = Depends(get_db)):
    return db.query(Stock).filter(Stock.product_id == product_id).all()
