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
    IN = "IN"  # Entrada
    OUT = "OUT"  # Saída


# =========================
# Movimento de estoque
# =========================
class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
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

    # Relacionamento com produto
    product = relationship(
        "Product",
        back_populates="stock_movements"
    )


# =========================
# Produto (com estoque)
# =========================
class Product(Base):
    __tablename__ = "products"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name = Column(String(255), nullable=False)
    stock_quantity = Column(Float, default=0.0, nullable=False)

    # Relacionamento com movimentos de estoque
    stock_movements = relationship(
        "StockMovement",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    # =========================
    # Funções auxiliares de estoque
    # =========================
    def add_stock(self, quantity: float):
        """Registra entrada de estoque"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        movement = StockMovement(
            product_id=self.id,
            quantity=quantity,
            movement_type=StockMovementType.IN
        )
        self.stock_quantity += quantity
        return movement

    def remove_stock(self, quantity: float):
        """Registra saída de estoque"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if quantity > self.stock_quantity:
            raise ValueError("Insufficient stock to remove")
        movement = StockMovement(
            product_id=self.id,
            quantity=quantity,
            movement_type=StockMovementType.OUT
        )
        self.stock_quantity -= quantity
        return movement

    def get_stock_balance(self):
        """Retorna saldo atual do estoque"""
        return self.stock_quantity
