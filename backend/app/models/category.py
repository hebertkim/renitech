from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class ProductCategory(Base):
    __tablename__ = "product_categories"

    # Id da categoria
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Nome da categoria, com comprimento especificado
    name = Column(String(255), nullable=False)

    # Descrição da categoria, também com comprimento especificado
    description = Column(String(500), nullable=True)

    # Relação com os produtos
    products = relationship("Product", back_populates="category")
