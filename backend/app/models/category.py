# app/models/category.py
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid

# =========================
# ProductCategory
# =========================
class ProductCategory(Base):
    __tablename__ = "product_categories"

    # Identificador único da categoria (UUID)
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )

    # Nome da categoria
    name = Column(String(255), nullable=False)

    # Descrição da categoria
    description = Column(String(500), nullable=True)

    # Código interno opcional para ERP
    code = Column(String(50), unique=True, nullable=True)

    # Status ativo/inativo
    is_active = Column(Boolean, default=True)

    # =========================
    # Auditoria / Multi-tenant
    # =========================
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    company_id = Column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    store_id = Column(String(36), ForeignKey("stores.id", ondelete="SET NULL"), nullable=True)

    # Relação com produtos
    products = relationship("Product", back_populates="category")
