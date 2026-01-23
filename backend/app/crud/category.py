from sqlalchemy.orm import Session
from app.models.category import ProductCategory
from app.schemas.category import ProductCategoryCreate, ProductCategoryUpdate
from uuid import uuid4

# =========================
# CREATE
# =========================
def create_category(db: Session, category_data: ProductCategoryCreate):
    db_category = ProductCategory(
        id=str(uuid4()),  # Gerar UUID como string
        name=category_data.name,
        description=category_data.description,
        code=category_data.code,
        is_active=category_data.is_active
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# =========================
# READ
# =========================
def get_category(db: Session, category_id: str):
    return db.query(ProductCategory).filter(ProductCategory.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductCategory).offset(skip).limit(limit).all()

# =========================
# UPDATE
# =========================
def update_category(db: Session, category_id: str, category_data: ProductCategoryUpdate):
    db_category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
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
def delete_category(db: Session, category_id: str):
    db_category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
    if not db_category:
        return None

    db.delete(db_category)
    db.commit()
    return db_category
