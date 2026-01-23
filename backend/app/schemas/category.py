from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from datetime import datetime
from app.schemas import product as product_schemas

# =========================
# Base da categoria
# =========================
class ProductCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    code: Optional[str] = None
    is_active: bool = True

# =========================
# Modelo para criação
# =========================
class ProductCategoryCreate(ProductCategoryBase):
    pass

# =========================
# Modelo para atualização
# =========================
class ProductCategoryUpdate(ProductCategoryBase):
    pass

# =========================
# Modelo para leitura
# =========================
class ProductCategory(ProductCategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    # Lista de produtos relacionados (opcional)
    products: Optional[List[product_schemas.Product]] = []

    class Config:
        orm_mode = True
