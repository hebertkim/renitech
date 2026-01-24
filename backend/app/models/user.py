# app/models/user.py

from sqlalchemy import Column, String, DateTime, Float
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
        default=lambda: str(uuid.uuid4()))

    # =========================
    # Dados do usuário
    # =========================
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)  # hashed

    # Avatar: guarda SOMENTE o caminho da imagem
    avatar = Column(String(500), nullable=True)

    # =========================
    # Campos financeiros / controle
    # =========================
    balance = Column(Float, default=0)

    # =========================
    # Auditoria
    # =========================
    created_at = Column(DateTime, default=datetime.utcnow)
