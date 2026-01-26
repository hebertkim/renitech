# app/models/user.py

from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = "users"

    # ==========================
    # IDENTIFICAÇÃO
    # ==========================
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)  # hashed
    avatar = Column(String(500), nullable=True)

    # ==========================
    # FINANCEIRO
    # ==========================
    balance = Column(Numeric(12, 2), default=0.0)  # mais seguro para valores monetários

    # ==========================
    # ROLE DO USUÁRIO
    # ==========================
    # cliente | vendedor | admin | superadmin
    role = Column(String(50), default="cliente", nullable=False)

    # ==========================
    # MULTI-TENANT
    # ==========================
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    store_id = Column(String(36), ForeignKey("stores.id", ondelete="SET NULL"), nullable=True)

    company = relationship("app.models.company.Company", back_populates="users")
    store = relationship("app.models.store.Store", back_populates="users")

    # ==========================
    # RELACIONAMENTOS
    # ==========================
    orders = relationship(
        "app.models.order.Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # ==========================
    # CONTROLE DE DATAS
    # ==========================
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # ==========================
    # PROPRIEDADE AUXILIAR MULTI-TENANT
    # ==========================
    @property
    def tenant_id(self):
        """
        Retorna a identificação principal do tenant (empresa ou loja) para simplificar queries.
        """
        return self.company_id or self.store_id

    # ==========================
    # SERIALIZAÇÃO MANUAL
    # ==========================
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "avatar": self.avatar,
            "balance": float(self.balance) if self.balance is not None else 0.0,
            "role": self.role,
            "company_id": self.company_id,
            "store_id": self.store_id,
            "tenant_id": self.tenant_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
