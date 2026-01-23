# app/crud/stock.py
from sqlalchemy.orm import Session
from app.models.stock import StockMovement, StockMovementType
from app.models.product import Product
from app.schemas import stock as schemas
from fastapi import HTTPException

# =========================
# Adicionar estoque (entrada)
# =========================
def add_stock(db: Session, product_id: str, quantity: float) -> StockMovement:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Cria movimento de entrada
    stock_entry = StockMovement(
        product_id=product_id,
        quantity=quantity,
        movement_type=StockMovementType.IN
    )
    db.add(stock_entry)

    # Atualiza estoque do produto
    product.stock_quantity += quantity
    db.commit()
    db.refresh(stock_entry)

    return stock_entry

# =========================
# Remover estoque (saída)
# =========================
def remove_stock(db: Session, product_id: str, quantity: float) -> StockMovement:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if product.stock_quantity < quantity:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")

    # Cria movimento de saída
    stock_exit = StockMovement(
        product_id=product_id,
        quantity=quantity,
        movement_type=StockMovementType.OUT
    )
    db.add(stock_exit)

    # Atualiza estoque do produto
    product.stock_quantity -= quantity
    db.commit()
    db.refresh(stock_exit)

    return stock_exit

# =========================
# Listar movimentos de um produto
# =========================
def get_stock_movements(db: Session, product_id: str):
    return db.query(StockMovement).filter(StockMovement.product_id == product_id).order_by(StockMovement.created_at.desc()).all()
