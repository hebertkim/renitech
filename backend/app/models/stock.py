# app/models/stock.py

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
import enum
from datetime import datetime


# =========================
# Tipo de movimento
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
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )

    # =========================
    # Relacionamento com Produto
    # =========================
    product_id = Column(
        String(36),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )
    product = relationship(
        "Product",
        back_populates="stock_movements"
    )

    # =========================
    # Quantidade e tipo
    # =========================
    quantity = Column(Float, nullable=False)
    movement_type = Column(Enum(StockMovementType), nullable=False)

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
