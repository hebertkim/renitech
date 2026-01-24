from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, relationship
from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    Numeric,
)
from sqlalchemy.sql import func
from app.database import Base, get_db
from PIL import Image
import uuid
import os
import hashlib

# Diretório para upload de imagens
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================
# Product
# =========================
class Product(Base):
    __tablename__ = "products"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    stock_quantity = Column(Float, default=0)
    stock_minimum = Column(Float, default=0)
    price_promotion = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    is_combo = Column(Boolean, default=False)
    show_in_promotion = Column(Boolean, default=False)
    no_stock_control = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    category_id = Column(String(36), ForeignKey("product_categories.id"))
    category = relationship(
        "ProductCategory",
        back_populates="products"
    )

    icms = Column(Numeric(10, 2), nullable=True)
    ipi = Column(Numeric(10, 2), nullable=True)
    pis = Column(Numeric(10, 2), nullable=True)
    cofins = Column(Numeric(10, 2), nullable=True)

    # Relação com imagens
    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan"
    )


# =========================
# ProductImage
# =========================
class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    product_id = Column(String(36), ForeignKey("products.id"))
    image_url = Column(String(500), nullable=False)

    product = relationship(
        "Product",
        back_populates="images"
    )


# =========================
# FastAPI Router para produtos e imagens
# =========================
router = APIRouter(prefix="/products", tags=["Products"])


# -------------------------
# Upload de imagem
# -------------------------
@router.post("/{product_id}/images")
async def upload_product_image(
    product_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Gera nome único com hash e converte para .webp
    file_content = await file.read()
    hash_name = hashlib.sha256(file_content).hexdigest() + ".webp"
    file_path = os.path.join(UPLOAD_DIR, hash_name)

    # Salva a imagem em .webp
    file.file.seek(0)
    image = Image.open(file.file)
    image.save(file_path, format="WEBP")

    # Salva registro no banco
    product_image = ProductImage(
        product_id=product.id,
        image_url=file_path
    )
    db.add(product_image)
    db.commit()
    db.refresh(product_image)

    return JSONResponse(
        {
            "id": product_image.id,
            "image_url": product_image.image_url
        }
    )


# -------------------------
# Listar imagens do produto
# -------------------------
@router.get("/{product_id}/images")
def list_product_images(
    product_id: str,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return [
        {"id": img.id, "image_url": img.image_url}
        for img in product.images
    ]


# -------------------------
# Remover imagem
# -------------------------
@router.delete("/images/{image_id}")
def delete_product_image(
    image_id: str,
    db: Session = Depends(get_db)
):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Remove arquivo físico
    if os.path.exists(image.image_url):
        os.remove(image.image_url)

    db.delete(image)
    db.commit()
    return JSONResponse({"detail": "Image deleted"})
