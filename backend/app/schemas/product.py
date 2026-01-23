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
    images: Optional[List[str]] = []  # URLs de imagens na criação

# =========================
# Modelo para atualização
# =========================
class ProductUpdate(ProductBase):
    images: Optional[List[str]] = []  # Permite atualizar imagens

# =========================
# Modelo para leitura
# =========================
class Product(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    images: Optional[List[str]] = []  # Lista de URLs das imagens

    class Config:
        orm_mode = True  # Compatibilidade com SQLAlchemy
