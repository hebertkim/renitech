# app/models/user.py

from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid


class User(Base):
    __tablename__ = "users"

    # =========================
    # Primary Key (UUID)
    # =========================
    id = Column(
        String(36),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )

    # =========================
    # Dados do usuário
    # =========================
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)  # hashed
    avatar = Column(String(500), nullable=True)

    # =========================
    # Controle financeiro / extras
    # =========================
    balance = Column(Float, default=0)

    # =========================
    # Multi-Tenant
    # =========================
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True)
    store_id = Column(String(36), ForeignKey("stores.id"), nullable=True)
    company = relationship("Company", back_populates="users")
    store = relationship("Store", back_populates="users")

    # =========================
    # Permissões / Roles
    # =========================
    role = Column(String(50), default="user")  # user, admin, manager

    # =========================
    # Auditoria
    # =========================
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
