# app/models/stock.py

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
import enum
from datetime import datetime

# =========================
# Tipo de movimento de estoque
# =========================
class StockMovementType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"

# =========================
# Movimento de estoque
# =========================
class StockMovement(Base):
    __tablename__ = "stock_movements"

    # =========================
    # Primary Key
    # =========================
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    # =========================
    # Relacionamento com Produto
    # =========================
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    product = relationship("Product", back_populates="stock_movements")

    # =========================
    # Quantidade e tipo de movimento
    # =========================
    quantity = Column(Float, nullable=False)
    movement_type = Column(Enum(StockMovementType), nullable=False)

    # =========================
    # Multi-Tenant
    # =========================
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True, index=True)
    store_id = Column(String(36), ForeignKey("stores.id"), nullable=True, index=True)

    # =========================
    # Auditoria
    # =========================
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # =========================
    # Propriedade auxiliar multi-tenant
    # =========================
    @property
    def tenant_id(self):
        """
        Retorna o tenant principal do movimento (empresa).
        """
        return self.company_id

    # =========================
    # Serialização manual
    # =========================
    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "movement_type": self.movement_type.value,
            "company_id": self.company_id,
            "store_id": self.store_id,
            "tenant_id": self.tenant_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
