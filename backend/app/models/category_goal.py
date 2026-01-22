from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CategoryGoal(Base):
    __tablename__ = "category_goals"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=False)  # ✅ Corrigido
    target_amount = Column(Numeric(10, 2), nullable=False)  # ✅ Numeric para valores monetários
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    # Relacionamento opcional com Category
    category = relationship("Category", back_populates="goals")
