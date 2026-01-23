from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

# Base do Produto com os campos comuns
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    sku: str  # SKU como campo obrigatório
    stock_quantity: int
    is_active: bool = True

# Modelo para criação de um produto
class ProductCreate(ProductBase):
    pass

# Modelo para atualização de um produto
class ProductUpdate(ProductBase):
    pass

# Modelo para leitura de um produto (inclui id e timestamps)
class Product(ProductBase):
    id: UUID  # Usando UUID para o id
    created_at: datetime  # Usando datetime para a data de criação
    updated_at: datetime  # Usando datetime para a data de atualização

    class Config:
        orm_mode = True  # Habilita a compatibilidade com os modelos do SQLAlchemy
