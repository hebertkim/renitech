# app/models/product.py

from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid
from datetime import datetime


class Product(Base):
    __tablename__ = "products"

    # =========================
    # Primary Key
    # =========================
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )

    # =========================
    # Dados do produto
    # =========================
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    sku = Column(String(100), unique=True, index=True, nullable=False)

    stock_quantity = Column(Float, default=0)
    stock_minimum = Column(Float, default=0)

    price_promotion = Column(Float, nullable=True)

    is_active = Column(Boolean, default=True)
    is_combo = Column(Boolean, default=False)
    show_in_promotion = Column(Boolean, default=False)
    no_stock_control = Column(Boolean, default=False)

    # =========================
    # Multi-Tenant
    # =========================
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True)
    store_id = Column(String(36), ForeignKey("stores.id"), nullable=True)

    # =========================
    # Auditoria
    # =========================
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # =========================
    # Relacionamentos
    # =========================
    category_id = Column(String(36), ForeignKey("product_categories.id"))
    category = relationship(
        "ProductCategory",
        back_populates="products"
    )

    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    stock_movements = relationship(
        "StockMovement",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    # =========================
    # Impostos
    # =========================
    icms = Column(Numeric(10, 2), nullable=True)
    ipi = Column(Numeric(10, 2), nullable=True)
    pis = Column(Numeric(10, 2), nullable=True)
    cofins = Column(Numeric(10, 2), nullable=True)
