# app/crud/product.py
from sqlalchemy.orm import Session
from app.models.product import Product, ProductImage
from app.schemas import product as schemas
from app.security.tenant import Tenant
from uuid import uuid4
import os

# =========================
# CREATE
# =========================
def create_product(db: Session, product_data: schemas.ProductCreate, tenant: Tenant):
    """
    Cria um produto vinculado ao tenant do usuário (company_id + store_id).
    """
    images_data = getattr(product_data, "images", [])
    product_dict = product_data.dict(exclude={"images"})

    # Adiciona automaticamente os IDs do tenant
    product_dict["company_id"] = tenant.company_id
    product_dict["store_id"] = tenant.store_id

    db_product = Product(**product_dict)
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


# =========================
# READ
# =========================
def get_product(db: Session, product_id: str, tenant: Tenant):
    """
    Retorna um produto específico do tenant.
    """
    return (
        db.query(Product)
        .filter(Product.id == product_id, Product.company_id == tenant.company_id)
        .first()
    )


def get_products(db: Session, tenant: Tenant, skip: int = 0, limit: int = 100):
    """
    Retorna todos os produtos do tenant, com paginação.
    """
    return (
        db.query(Product)
        .filter(Product.company_id == tenant.company_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# =========================
# UPDATE
# =========================
def update_product(db: Session, product_id: str, product_data: schemas.ProductUpdate, tenant: Tenant):
    """
    Atualiza um produto existente, somente dentro do tenant.
    """
    db_product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.company_id == tenant.company_id)
        .first()
    )
    if not db_product:
        return None

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


# =========================
# DELETE
# =========================
def delete_product(db: Session, product_id: str, tenant: Tenant):
    """
    Deleta um produto e suas imagens, apenas dentro do tenant.
    """
    db_product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.company_id == tenant.company_id)
        .first()
    )
    if not db_product:
        return None

    images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
    for img in images:
        if os.path.exists(img.image_url):
            os.remove(img.image_url)
        db.delete(img)

    db.delete(db_product)
    db.commit()
    return db_product
