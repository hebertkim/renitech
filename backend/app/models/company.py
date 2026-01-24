# app/models/company.py

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid

class Company(Base):
    __tablename__ = "companies"

    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    # Dados da empresa
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)

    # Auditoria
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # =========================
    # Relacionamentos com Stores
    # =========================
    stores = relationship("Store", back_populates="company", cascade="all, delete-orphan")

    # Relacionamentos diretos (opcional)
    users = relationship("User", back_populates="company")
    products = relationship("Product", back_populates="company")
    customers = relationship("Customer", back_populates="company")
    orders = relationship("Order", back_populates="company")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "stores": [store.to_dict() for store in self.stores]
        }
