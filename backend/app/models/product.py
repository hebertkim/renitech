# app/models/product.py

from sqlalchemy import Column, String, Float, Boolean, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid

class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
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

    # Multi-tenant
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    store_id = Column(String(36), ForeignKey("stores.id", ondelete="SET NULL"), nullable=True)

    company = relationship("Company", back_populates="products")
    store = relationship("Store", back_populates="products")

    # Categoria
    category_id = Column(String(36), ForeignKey("product_categories.id"))
    category = relationship("ProductCategory", back_populates="products")

    # Impostos
    icms = Column(Numeric(10, 2), nullable=True)
    ipi = Column(Numeric(10, 2), nullable=True)
    pis = Column(Numeric(10, 2), nullable=True)
    cofins = Column(Numeric(10, 2), nullable=True)

    # Relacionamentos
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    stock_movements = relationship("StockMovement", back_populates="product", cascade="all, delete-orphan")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "sku": self.sku,
            "stock_quantity": self.stock_quantity,
            "stock_minimum": self.stock_minimum,
            "price_promotion": self.price_promotion,
            "is_active": self.is_active,
            "is_combo": self.is_combo,
            "show_in_promotion": self.show_in_promotion,
            "no_stock_control": self.no_stock_control,
            "company_id": self.company_id,
            "store_id": self.store_id,
            "category_id": self.category_id,
            "images": [img.to_dict() for img in self.images],
            "icms": float(self.icms) if self.icms else None,
            "ipi": float(self.ipi) if self.ipi else None,
            "pis": float(self.pis) if self.pis else None,
            "cofins": float(self.cofins) if self.cofins else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
