# app/schemas/order.py

from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from datetime import datetime
from uuid import UUID

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
    product_id: UUID
    quantity: float


class OrderItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity: float
    unit_price: float
    subtotal: float

    model_config = {
        "from_attributes": True
    }


# =========================
# Pedido
# =========================

class OrderCreate(BaseModel):
    user_id: UUID
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: OrderStatus
    total: float
    items: List[OrderItemResponse]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# =========================
# Atualização do status do pedido
# =========================

class OrderStatusUpdate(BaseModel):
    status: OrderStatus


# =========================
# Histórico de status do pedido
# =========================

class OrderStatusHistory(BaseModel):
    status: OrderStatus
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


# =========================
# 🔥 ALIAS DE COMPATIBILIDADE
# =========================

# Permite: from app.schemas.order import Order
Order = OrderResponse
OrderItem = OrderItemResponse
