import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, JSON, CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    # ID UUID como CHAR(36) para MySQL
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)

    # Campos básicos
    name = Column(String(100), nullable=False, unique=True)
    type = Column(Enum("income", "expense", "transfer", name="category_type"), nullable=False)

    # Subcategoria
    parent_id = Column(CHAR(36), ForeignKey("categories.id"), nullable=True)
    parent = relationship("Category", remote_side=[id], backref="subcategories")

    # Campos adicionais
    description = Column(String(255), nullable=True)
    fiscal_class = Column(String(50), nullable=True)
    ai_rules = Column(JSON, nullable=True)

    # Relacionamentos com despesas, receitas e metas
    expenses = relationship(
        "Expense",
        back_populates="category",
        cascade="all, delete-orphan"
    )
    incomes = relationship(
        "Income",
        back_populates="category",
        cascade="all, delete-orphan"
    )
    goals = relationship(
        "CategoryGoal",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    # Histórico de criação/atualização
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
