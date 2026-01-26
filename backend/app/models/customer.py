# app/models/customer.py

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True)

    # =========================
    # Multi-tenant
    # =========================
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    store_id = Column(String(36), ForeignKey("stores.id", ondelete="SET NULL"), nullable=True, index=True)

    company = relationship("Company", back_populates="customers")
    store = relationship("Store", back_populates="customers")

    # =========================
    # Relacionamentos
    # =========================
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")

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
            "name": self.name,
            "email": self.email,
            "company_id": self.company_id,
            "store_id": self.store_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
