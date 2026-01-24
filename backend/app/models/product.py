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


class Product(Base):
    __tablename__ = "products"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()))

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

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    category_id = Column(String(36), ForeignKey("product_categories.id"))
    category = relationship(
        "ProductCategory",
        back_populates="products"
    )

    icms = Column(Numeric(10, 2), nullable=True)
    ipi = Column(Numeric(10, 2), nullable=True)
    pis = Column(Numeric(10, 2), nullable=True)
    cofins = Column(Numeric(10, 2), nullable=True)

    # Imagens
    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    # Movimentos de estoque
    stock_movements = relationship(
        "StockMovement",
        back_populates="product",
        cascade="all, delete-orphan"
    )
