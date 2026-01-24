# app/schemas/product.py

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

# =========================
# Base do Produto
# =========================

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    sku: str

    stock_quantity: float
    stock_minimum: Optional[float] = 0

    price_promotion: Optional[float] = None

    is_active: bool = True
    is_combo: bool = False
    show_in_promotion: bool = False
    no_stock_control: bool = False

    category_id: Optional[UUID] = None

    # Impostos
    icms: Optional[float] = None
    ipi: Optional[float] = None
    pis: Optional[float] = None
    cofins: Optional[float] = None


# =========================
# Modelo para criação
# =========================

class ProductCreate(ProductBase):
    images: Optional[List[str]] = Field(default_factory=list)


# =========================
# Modelo para atualização
# =========================

class ProductUpdate(ProductBase):
    images: Optional[List[str]] = Field(default_factory=list)


# =========================
# Modelo de imagem (interno)
# =========================

class ProductImageSchema(BaseModel):
    id: UUID
    image_url: str

    model_config = {
        "from_attributes": True
    }


# =========================
# Modelo para leitura (response)
# =========================

class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    images: List[str] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }


# =========================
# 🔥 ALIAS PARA COMPATIBILIDADE COM AS ROTAS
# =========================

# Agora: from app.schemas.product import Product FUNCIONA
Product = ProductResponse


# =========================
# Função auxiliar ORM -> Schema
# =========================

def product_to_schema(product) -> ProductResponse:
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        sku=product.sku,
        stock_quantity=product.stock_quantity,
        stock_minimum=product.stock_minimum,
        price_promotion=product.price_promotion,
        is_active=product.is_active,
        is_combo=product.is_combo,
        show_in_promotion=product.show_in_promotion,
        no_stock_control=product.no_stock_control,
        category_id=product.category_id,
        icms=product.icms,
        ipi=product.ipi,
        pis=product.pis,
        cofins=product.cofins,
        created_at=product.created_at,
        updated_at=product.updated_at,
        images=[img.image_url for img in getattr(product, "images", []) or []],
    )
