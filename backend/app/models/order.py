from sqlalchemy import Column, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid
from enum import Enum as PyEnum


# =========================
# Status do pedido
# =========================
class OrderStatus(str, PyEnum):
    PENDING = "Pendente"
    PAID = "Pago"
    SHIPPED = "Enviado"
    CANCELLED = "Cancelado"


# =========================
# Pedido
# =========================
class Order(Base):
    __tablename__ = "orders"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    user_id = Column(String(36), nullable=False)
    status = Column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING
    )
    total = Column(Float, default=0.0)
    created_at = Column(DateTime, default=func.now())

    # Relacionamento com itens do pedido
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade=(
            "all, delete-orphan"
        )
    )


# =========================
# Item do pedido
# =========================
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    order_id = Column(String(36), ForeignKey("orders.id"))
    product_id = Column(String(36), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relacionamento com pedido
    order = relationship("Order", back_populates="items")
