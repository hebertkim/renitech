from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.stock import StockMovement, StockMovementType
from app.models.product import Product
from app.security.tenant import Tenant  # objeto tenant do usuário logado


# =========================
# Adicionar estoque (entrada)
# =========================
def add_stock(db: Session, product_id: str, quantity: float, tenant: Tenant) -> StockMovement:
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.company_id == tenant.company_id,
        Product.store_id == tenant.store_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado ou fora do seu tenant")

    # Garante que stock_quantity não seja None
    if product.stock_quantity is None:
        product.stock_quantity = 0

    # Atualiza estoque do produto
    product.stock_quantity += quantity

    # Cria movimento de entrada com tenant
    stock_entry = StockMovement(
        product_id=product_id,
        quantity=quantity,
        movement_type=StockMovementType.IN,
        company_id=tenant.company_id,
        store_id=tenant.store_id
    )

    db.add(stock_entry)
    db.add(product)
    db.commit()
    db.refresh(stock_entry)
    return stock_entry


# =========================
# Remover estoque (saída)
# =========================
def remove_stock(db: Session, product_id: str, quantity: float, tenant: Tenant) -> StockMovement:
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.company_id == tenant.company_id,
        Product.store_id == tenant.store_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado ou fora do seu tenant")

    if product.stock_quantity is None:
        product.stock_quantity = 0

    if product.stock_quantity < quantity:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")

    # Atualiza estoque do produto
    product.stock_quantity -= quantity

    # Cria movimento de saída com tenant
    stock_exit = StockMovement(
        product_id=product_id,
        quantity=quantity,
        movement_type=StockMovementType.OUT,
        company_id=tenant.company_id,
        store_id=tenant.store_id
    )

    db.add(stock_exit)
    db.add(product)
    db.commit()
    db.refresh(stock_exit)
    return stock_exit


# =========================
# Listar movimentos de um produto
# =========================
def get_stock_movements(db: Session, product_id: str, tenant: Tenant):
    return (
        db.query(StockMovement)
        .filter(
            StockMovement.product_id == product_id,
            StockMovement.company_id == tenant.company_id,
            StockMovement.store_id == tenant.store_id
        )
        .order_by(StockMovement.created_at.desc())
        .all()
    )
