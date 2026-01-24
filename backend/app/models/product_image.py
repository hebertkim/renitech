# app/models/product_image.py

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid


class ProductImage(Base):
    __tablename__ = "product_images"

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
    # Relacionamento com produto
    # =========================
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    product = relationship(
        "Product",
        back_populates="images"
    )

    # =========================
    # Dados da imagem
    # =========================
    image_url = Column(String(500), nullable=False)

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
    # Métodos auxiliares
    # =========================
    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "image_url": self.image_url,
            "company_id": self.company_id,
            "store_id": self.store_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
