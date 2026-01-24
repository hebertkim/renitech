# app/schemas/stock.py

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

# =========================
# Base do estoque
# =========================

class StockBase(BaseModel):
    product_id: UUID
    quantity: float = 0
    min_quantity: float = 0
    location: Optional[str] = None
    is_active: bool = True


# =========================
# Criar / atualizar estoque
# =========================

class StockCreate(StockBase):
    pass


class StockUpdate(BaseModel):
    quantity: Optional[float] = None
    min_quantity: Optional[float] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None


# =========================
# Resposta do estoque
# =========================

class StockResponse(StockBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


# =========================
# 🔥 ALIAS DE COMPATIBILIDADE
# =========================

# Permite: from app.schemas.stock import Stock
Stock = StockResponse
