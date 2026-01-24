from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


class Customer(Base):
    __tablename__ = "customers"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)

    orders = relationship("Order", back_populates="customer")
