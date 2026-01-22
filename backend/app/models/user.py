from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # hashed

    # ✅ Avatar: guarda SOMENTE o caminho da imagem
    avatar = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    balance = Column(Float, default=0)

    # ==========================
    # Relacionamentos
    # ==========================
    expenses = relationship("Expense", back_populates="user")
    incomes = relationship("Income", back_populates="user")  # 🔹 Adicionado para receitas
