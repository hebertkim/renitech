# app/crud/product.py
from sqlalchemy.orm import Session
from app.models.product import Product  # Importando o modelo de produto
from app.schemas import product as schemas

def create_product(db: Session, product_data: schemas.ProductCreate):  # Alterado para ProductCreate
    # Converte o objeto product_data para um dicionário com .dict()
    db_product = Product(**product_data.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: str):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: str, product_data: dict):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        for key, value in product_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    return None

def delete_product(db: Session, product_id: str):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return db_product
    return None
