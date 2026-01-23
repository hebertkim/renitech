from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func  # Importação do 'func' para usar 'func.now()'
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
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())  # Agora 'func.now()' está funcionando corretamente
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Definições de relacionamento
    category_id = Column(String(36), ForeignKey("product_categories.id"))  # Corrigido com 'ForeignKey'
    category = relationship("ProductCategory", back_populates="products")  # Alterado para 'back_populates'
