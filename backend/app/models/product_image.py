# app/models/product_image.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()))

    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    image_url = Column(String(500), nullable=False)

    product = relationship(
        "Product",
        back_populates="images"
    )
