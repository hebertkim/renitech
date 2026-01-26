# app/models/order.py

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid
import enum

# =========================
# Enum para status do pedido
# =========================
class OrderStatus(str, enum.Enum):
    PENDING = "Pendente"
    PAID = "Pago"
    SHIPPED = "Enviado"
    CANCELLED = "Cancelado"

# =========================
# Pedido
# =========================
class Order(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True, index=True)
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    store_id = Column(String(36), ForeignKey("stores.id", ondelete="SET NULL"), nullable=True, index=True)

    total = Column(Float, default=0.0, nullable=False)
    status = Column(Enum(OrderStatus, name="order_status_enum"), default=OrderStatus.PENDING, nullable=False)

    # Relacionamentos
    user = relationship("User", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")
    company = relationship("Company", back_populates="orders")
    store = relationship("Store", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # =========================
    # Propriedade auxiliar multi-tenant
    # =========================
    @property
    def tenant_id(self):
        return self.company_id

    # =========================
    # Serialização
    # =========================
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "customer_id": self.customer_id,
            "total": self.total,
            "status": self.status.value,
            "company_id": self.company_id,
            "store_id": self.store_id,
            "tenant_id": self.tenant_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "items": [item.to_dict() for item in self.items],
        }

# =========================
# Item do Pedido
# =========================
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    order_id = Column(String(36), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="RESTRICT"), nullable=False, index=True)
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    store_id = Column(String(36), ForeignKey("stores.id", ondelete="SET NULL"), nullable=True, index=True)

    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relacionamentos
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
    company = relationship("Company")
    store = relationship("Store")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # =========================
    # Propriedade auxiliar multi-tenant
    # =========================
    @property
    def tenant_id(self):
        return self.company_id

    # =========================
    # Serialização
    # =========================
    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "subtotal": self.subtotal,
            "company_id": self.company_id,
            "store_id": self.store_id,
            "tenant_id": self.tenant_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

# =========================
# Índices adicionais para consultas multi-tenant
# =========================
Index("idx_order_company_store", Order.company_id, Order.store_id)
Index("idx_order_item_company_store", OrderItem.company_id, OrderItem.store_id)
