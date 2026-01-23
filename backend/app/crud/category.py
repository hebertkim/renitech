from sqlalchemy.orm import Session
from app.models.category import ProductCategory
from app.schemas.category import ProductCategorySchema
from uuid import uuid4

# Função para criar uma categoria
def create_category(db: Session, category_data: ProductCategorySchema):
    db_category = ProductCategory(
        id=uuid4(),  # Gerar um UUID único para a categoria
        name=category_data.name,
        description=category_data.description,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Função para obter uma categoria pelo ID
def get_category(db: Session, category_id: str):
    return db.query(ProductCategory).filter(ProductCategory.id == category_id).first()

# Função para obter todas as categorias com paginação
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductCategory).offset(skip).limit(limit).all()
