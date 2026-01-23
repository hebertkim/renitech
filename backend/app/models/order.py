# app/models/order.py
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid
import enum

# =========================
# Status do pedido
# =========================
class OrderStatus(str, enum.Enum):
    PENDING = "Pendente"
    PAID = "Pago"
    SHIPPED = "Enviado"
    CANCELLED = "Cancelado"

# =========================
# Item do pedido
# =========================
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String(36), ForeignKey("orders.id"))
    product_id = Column(String(36), ForeignKey("products.id"))
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relacionamento com produto
    product = relationship("Product")

# =========================
# Pedido
# =========================
class Order(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total = Column(Float, default=0.0)
    created_at = Column(DateTime, default=func.now())

    # Relacionamento com itens
    items = relationship("OrderItem", backref="order", cascade="all, delete-orphan")
