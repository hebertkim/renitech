# app/models/customer.py
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid


class Customer(Base):
    __tablename__ = "customers"

    # =========================
    # Primary Key (UUID)
    # =========================
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )

    # =========================
    # Dados do cliente
    # =========================
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True)

    # =========================
    # Auditoria / Multi-tenant
    # =========================
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    company_id = Column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    store_id = Column(String(36), ForeignKey("stores.id", ondelete="SET NULL"), nullable=True)

    # =========================
    # Relacionamentos
    # =========================
    orders = relationship("Order", back_populates="customer")
