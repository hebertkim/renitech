# app/schemas/stock.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

# =========================
# Tipo de movimento
# =========================


class StockMovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"


# =========================
# Schema para criar novo movimento
# =========================
class StockCreate(BaseModel):
    product_id: str
    quantity: float = Field(
        ...,
        gt=0,
        description="Quantidade deve ser maior que zero"
    )
    movement_type: StockMovementType
    created_at: Optional[
        datetime] = None  # opcional para importações ou testes

    @validator("quantity")
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be positive")
        return v


# =========================
# Schema usado para retornar movimentos
# =========================
class Stock(BaseModel):
    id: str
    product_id: str
    quantity: float
    movement_type: StockMovementType
    created_at: datetime

    class Config:
        orm_mode = True


# =========================
# Schema para retorno de múltiplos movimentos
# =========================
class StockList(BaseModel):
    movements: List[Stock]
