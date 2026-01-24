# app/models/stock.py
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
import enum


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

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()))

    product_id = Column(
        String(36),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )

    quantity = Column(Float, nullable=False)
    movement_type = Column(Enum(StockMovementType), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relacionamento
    product = relationship(
        "Product",
        back_populates="stock_movements"
    )
