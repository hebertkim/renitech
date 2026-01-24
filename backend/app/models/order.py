# app/models/order.py

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
import enum


# =========================
# Status do pedido
# =========================
class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELED = "CANCELED"
    SHIPPED = "SHIPPED"
    FINISHED = "FINISHED"


# =========================
# Pedido
# =========================
class Order(Base):
    __tablename__ = "orders"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()))

    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=True)

    total = Column(Float, default=0.0)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # =========================
    # Relacionamentos
    # =========================
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    customer = relationship(
        "Customer",
        back_populates="orders"
    )


# =========================
# Itens do pedido
# =========================
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()))

    order_id = Column(
        String(36),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )

    product_id = Column(
        String(36),
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    # =========================
    # Relacionamentos
    # =========================
    order = relationship(
        "Order",
        back_populates="items"
    )

    product = relationship("Product")
