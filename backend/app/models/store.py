# app/models/store.py

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid

class Store(Base):
    __tablename__ = "stores"

    # ==========================
    # IDENTIFICAÇÃO
    # ==========================
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    # ==========================
    # DADOS DA LOJA
    # ==========================
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)

    # ==========================
    # MULTI-TENANT
    # ==========================
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    company = relationship("Company", back_populates="stores")

    # ==========================
    # AUDITORIA
    # ==========================
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # ==========================
    # RELACIONAMENTOS INTERNOS
    # ==========================
    users = relationship("User", back_populates="store", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="store", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="store", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="store", cascade="all, delete-orphan")

    # ==========================
    # PROPRIEDADE AUXILIAR MULTI-TENANT
    # ==========================
    @property
    def tenant_id(self):
        """
        Retorna o tenant principal da loja (empresa).
        """
        return self.company_id

    # ==========================
    # SERIALIZAÇÃO MANUAL
    # ==========================
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "company_id": self.company_id,
            "tenant_id": self.tenant_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "users": [user.to_dict() for user in self.users],
            "products": [product.to_dict() for product in self.products],
            "customers": [customer.to_dict() for customer in self.customers],
            "orders": [order.to_dict() for order in self.orders],
        }
