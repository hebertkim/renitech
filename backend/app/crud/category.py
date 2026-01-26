# app/crud/category.py

from sqlalchemy.orm import Session
from app.models.category import ProductCategory
from app.schemas.category import ProductCategoryCreate, ProductCategoryUpdate
from app.security.tenant import Tenant
from uuid import uuid4
from typing import List, Optional

# =========================
# CREATE
# =========================
def create_category(db: Session, category_data: ProductCategoryCreate, tenant: Tenant) -> ProductCategory:
    """
    Cria uma nova categoria de produto vinculada ao tenant.
    """
    db_category = ProductCategory(
        id=str(uuid4()),
        name=category_data.name,
        description=category_data.description,
        code=category_data.code,
        is_active=category_data.is_active,
        company_id=tenant.company_id,
        store_id=tenant.store_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# =========================
# READ
# =========================
def get_category(db: Session, category_id: str, tenant: Tenant) -> Optional[ProductCategory]:
    """
    Retorna uma categoria pelo ID, dentro do tenant.
    """
    return (
        db.query(ProductCategory)
        .filter(
            ProductCategory.id == category_id,
            ProductCategory.company_id == tenant.company_id
        )
        .first()
    )


def get_categories(db: Session, tenant: Tenant, skip: int = 0, limit: int = 100) -> List[ProductCategory]:
    """
    Retorna uma lista de categorias do tenant, com paginação.
    """
    return (
        db.query(ProductCategory)
        .filter(ProductCategory.company_id == tenant.company_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# =========================
# UPDATE
# =========================
def update_category(db: Session, category_id: str, category_data: ProductCategoryUpdate, tenant: Tenant) -> Optional[ProductCategory]:
    """
    Atualiza os dados de uma categoria existente, apenas no tenant.
    """
    db_category = (
        db.query(ProductCategory)
        .filter(
            ProductCategory.id == category_id,
            ProductCategory.company_id == tenant.company_id
        )
        .first()
    )
    if not db_category:
        return None

    for key, value in category_data.dict(exclude_unset=True).items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


# =========================
# DELETE
# =========================
def delete_category(db: Session, category_id: str, tenant: Tenant) -> Optional[ProductCategory]:
    """
    Remove uma categoria pelo ID, apenas no tenant.
    """
    db_category = (
        db.query(ProductCategory)
        .filter(
            ProductCategory.id == category_id,
            ProductCategory.company_id == tenant.company_id
        )
        .first()
    )
    if not db_category:
        return None

    db.delete(db_category)
    db.commit()
    return db_category
