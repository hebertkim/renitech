# app/crud/product.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.product import Product, ProductImage
from app.schemas import product as schemas
from app.security.tenant import Tenant
from uuid import uuid4
import os

# =========================
# CREATE
# =========================
def create_product(db: Session, product_data: schemas.ProductCreate, tenant: Tenant) -> Product:
    """
    Cria um produto vinculado ao tenant do usuário (company_id + store_id) e suas imagens.
    """
    images_data = getattr(product_data, "images", [])
    product_dict = product_data.dict(exclude={"images"})
    product_dict["company_id"] = tenant.company_id
    product_dict["store_id"] = tenant.store_id

    db_product = Product(**product_dict)

    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        # Cria registros de imagens vinculadas
        for img_url in images_data:
            db_image = ProductImage(
                id=str(uuid4()),
                product_id=db_product.id,
                image_url=img_url,
                company_id=tenant.company_id,
                store_id=tenant.store_id
            )
            db.add(db_image)

        if images_data:
            db.commit()
            db.refresh(db_product)

        return db_product

    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Erro ao criar produto: {e.orig}") from e

# =========================
# READ
# =========================
def get_product(db: Session, product_id: str, tenant: Tenant) -> Product | None:
    """
    Retorna um produto específico do tenant.
    """
    return db.query(Product).filter(
        Product.id == product_id,
        Product.company_id == tenant.company_id,
        Product.store_id == tenant.store_id
    ).first()


def get_products(db: Session, tenant: Tenant, skip: int = 0, limit: int = 100) -> list[Product]:
    """
    Retorna todos os produtos do tenant, com paginação.
    """
    return db.query(Product).filter(
        Product.company_id == tenant.company_id,
        Product.store_id == tenant.store_id,
        Product.is_active == True  # filtra apenas produtos ativos
    ).offset(skip).limit(limit).all()

# =========================
# UPDATE
# =========================
def update_product(db: Session, product_id: str, product_data: schemas.ProductUpdate, tenant: Tenant) -> Product | None:
    """
    Atualiza um produto existente, incluindo imagens, somente dentro do tenant.
    """
    db_product = db.query(Product).filter(
        Product.id == product_id,
        Product.company_id == tenant.company_id,
        Product.store_id == tenant.store_id
    ).first()

    if not db_product:
        return None

    try:
        # Atualiza campos do produto
        for key, value in product_data.dict(exclude_unset=True, exclude={"images"}).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)

        # Atualiza imagens se fornecidas
        if hasattr(product_data, "images") and product_data.images is not None:
            old_images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
            for img in old_images:
                if os.path.exists(img.image_url):
                    os.remove(img.image_url)
                db.delete(img)
            db.commit()

            for img_url in product_data.images:
                db_image = ProductImage(
                    id=str(uuid4()),
                    product_id=product_id,
                    image_url=img_url,
                    company_id=tenant.company_id,
                    store_id=tenant.store_id
                )
                db.add(db_image)
            db.commit()
            db.refresh(db_product)

        return db_product

    except Exception as e:
        db.rollback()
        raise e

# =========================
# DELETE
# =========================
def delete_product(db: Session, product_id: str, tenant: Tenant) -> Product | None:
    """
    Deleta um produto e suas imagens, apenas dentro do tenant.
    """
    db_product = db.query(Product).filter(
        Product.id == product_id,
        Product.company_id == tenant.company_id,
        Product.store_id == tenant.store_id
    ).first()

    if not db_product:
        return None

    try:
        images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
        for img in images:
            if os.path.exists(img.image_url):
                os.remove(img.image_url)
            db.delete(img)

        db.delete(db_product)
        db.commit()
        return db_product

    except Exception as e:
        db.rollback()
        raise e
