# app/models/product.py
from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func
import uuid

# =========================
# Product
# =========================
class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    stock_quantity = Column(Float, default=0)
    stock_minimum = Column(Float, default=0)  # Estoque mínimo
    price_promotion = Column(Float, nullable=True)  # Preço promocional
    is_active = Column(Boolean, default=True)
    is_combo = Column(Boolean, default=False)  # Indica se é combo
    show_in_promotion = Column(Boolean, default=False)  # Exibição em promoções
    no_stock_control = Column(Boolean, default=False)  # Produto sem controle de estoque
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Categoria
    category_id = Column(String(36), ForeignKey("product_categories.id"))
    category = relationship("ProductCategory", back_populates="products")

    # Impostos
    icms = Column(Numeric(10, 2), nullable=True)
    ipi = Column(Numeric(10, 2), nullable=True)
    pis = Column(Numeric(10, 2), nullable=True)
    cofins = Column(Numeric(10, 2), nullable=True)

    # Relação com imagens
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")


# =========================
# ProductImage
# =========================
class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id"))
    image_url = Column(String(500), nullable=False)

    # Relacionamento inverso com Product
    product = relationship("Product", back_populates="images")
