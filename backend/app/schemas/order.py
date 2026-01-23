# app/schemas/order.py
from pydantic import BaseModel
from typing import List
from enum import Enum
from datetime import datetime

# =========================
# Status do pedido
# =========================
class OrderStatus(str, Enum):
    PENDING = "Pendente"
    PAID = "Pago"
    SHIPPED = "Enviado"
    CANCELLED = "Cancelado"

# =========================
# Item do pedido
# =========================
class OrderItemCreate(BaseModel):
    product_id: str
    quantity: float

class OrderItem(BaseModel):
    id: str
    product_id: str
    quantity: float
    unit_price: float
    subtotal: float

    class Config:
        orm_mode = True

# =========================
# Pedido
# =========================
class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItemCreate]

class Order(BaseModel):
    id: str
    user_id: str
    status: OrderStatus
    total: float
    items: List[OrderItem]
    created_at: datetime

    class Config:
        orm_mode = True
