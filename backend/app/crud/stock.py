from sqlalchemy.orm import Session
from app.models.product import Stock
from app.schemas import stock as schemas

# Registrar movimento de entrada de produto
def add_stock(db: Session, product_id: str, quantity: float):
    stock_entry = Stock(product_id=product_id, quantity_added=quantity, movement_type="entrada")
    db.add(stock_entry)
    db.commit()
    db.refresh(stock_entry)

    # Atualiza o estoque do produto
    product = db.query(Product).filter(Product.id == product_id).first()
    product.stock_quantity += quantity
    db.commit()

    return stock_entry

# Registrar movimento de saída de produto
def remove_stock(db: Session, product_id: str, quantity: float):
    stock_exit = Stock(product_id=product_id, quantity_removed=quantity, movement_type="saída")
    db.add(stock_exit)
    db.commit()
    db.refresh(stock_exit)

    # Atualiza o estoque do produto
    product = db.query(Product).filter(Product.id == product_id).first()
    product.stock_quantity -= quantity
    db.commit()

    return stock_exit
