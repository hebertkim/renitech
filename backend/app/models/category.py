from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func
import uuid

# =========================
# ProductCategory
# =========================
class ProductCategory(Base):
    __tablename__ = "product_categories"

    # Identificador único da categoria
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Nome da categoria
    name = Column(String(255), nullable=False)

    # Descrição da categoria
    description = Column(String(500), nullable=True)

    # Código interno opcional para ERP
    code = Column(String(50), unique=True, nullable=True)

    # Status ativo/inativo
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relação com produtos
    products = relationship("Product", back_populates="category")
