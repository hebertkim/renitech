# app/crud/product.py
from sqlalchemy.orm import Session
from app.models.product import Product, ProductImage
from app.schemas import product as schemas
from uuid import uuid4
import os

# =========================
# CREATE
# =========================
def create_product(db: Session, product_data: schemas.ProductCreate):
    # Extrai imagens da criação (se houver)
    images_data = product_data.images if hasattr(product_data, "images") else []
    product_dict = product_data.dict(exclude={"images"})

    db_product = Product(**product_dict)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Cria registros de imagens vinculadas
    for img_url in images_data:
        db_image = ProductImage(
            id=str(uuid4()),
            product_id=db_product.id,
            image_url=img_url
        )
        db.add(db_image)
    if images_data:
        db.commit()
        db.refresh(db_product)

    return db_product


# =========================
# READ
# =========================
def get_product(db: Session, product_id: str):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


# =========================
# UPDATE
# =========================
def update_product(db: Session, product_id: str, product_data: schemas.ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None

    # Atualiza campos do produto
    for key, value in product_data.dict(exclude_unset=True, exclude={"images"}).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)

    # Atualiza imagens se fornecidas
    if hasattr(product_data, "images") and product_data.images is not None:
        # Remove imagens antigas do banco e arquivos físicos
        old_images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
        for img in old_images:
            if os.path.exists(img.image_url):
                os.remove(img.image_url)
            db.delete(img)
        db.commit()

        # Adiciona novas imagens
        for img_url in product_data.images:
            db_image = ProductImage(
                id=str(uuid4()),
                product_id=product_id,
                image_url=img_url
            )
            db.add(db_image)
        db.commit()
        db.refresh(db_product)

    return db_product


# =========================
# DELETE
# =========================
def delete_product(db: Session, product_id: str):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None

    # Remove imagens associadas e arquivos físicos
    images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
    for img in images:
        if os.path.exists(img.image_url):
            os.remove(img.image_url)
        db.delete(img)

    db.delete(db_product)
    db.commit()
    return db_product
