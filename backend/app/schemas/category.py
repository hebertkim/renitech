# app/schemas/category.py

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List
from datetime import datetime

# Import atrasado para evitar problemas de import circular
from app.schemas.product import ProductResponse

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
# Modelo para leitura (response)
# =========================

class ProductCategoryResponse(ProductCategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    # Lista de produtos relacionados
    products: List[ProductResponse] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }


# =========================
# 🔥 ALIAS DE COMPATIBILIDADE (NÃO REMOVER)
# =========================

# Permite: from app.schemas.category import ProductCategory
ProductCategory = ProductCategoryResponse
