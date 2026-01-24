# app/schemas/product.py
from pydantic import BaseModel
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
    stock_minimum: Optional[float] = 0  # Estoque mínimo
    price_promotion: Optional[float] = None  # Preço promocional
    is_active: bool = True
    is_combo: bool = False  # Indica se é combo
    show_in_promotion: bool = False  # Exibir em promoções
    no_stock_control: bool = False  # Produto sem controle de estoque
    category_id: Optional[UUID] = None  # Categoria do produto
    icms: Optional[float] = None
    ipi: Optional[float] = None
    pis: Optional[float] = None
    cofins: Optional[float] = None


# =========================
# Modelo para criação
# =========================
class ProductCreate(ProductBase):
    # Para criação, podemos enviar URLs iniciais (opcional)
    images: Optional[List[str]] = []


# =========================
# Modelo para atualização
# =========================
class ProductUpdate(ProductBase):
    images: Optional[List[str]] = []  # Permite atualizar imagens


# =========================
# Modelo de imagem (para retorno)
# =========================
class ProductImageSchema(BaseModel):
    id: UUID
    image_url: str

    class Config:
        orm_mode = True


# =========================
# Modelo para leitura
# =========================
class Product(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    # Retorna somente URLs das imagens
    images: Optional[List[str]] = []

    class Config:
        orm_mode = True


# =========================
# Função auxiliar para converter Product + imagens do ORM para schema
# =========================
def product_to_schema(product) -> Product:
    return Product(
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
        images=[img.image_url for img in getattr(product, "images", [])]
    )
