# app/routes/products.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app import crud
from app.database import get_db
from app.schemas.product import (
    Product,
    ProductCreate,
    ProductUpdate,
    product_to_schema
)
from app.models.product_image import ProductImage

import os
import hashlib
from PIL import Image  # Certifique-se de ter 'pillow' instalado na venv

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==============================
# Router
# ==============================
router = APIRouter(prefix="/products", tags=["Products"])


# =========================
# PRODUTOS CRUD
# =========================
@router.get("/products/", response_model=List[Product])
def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    products = crud.get_products(db=db, skip=skip, limit=limit)
    return [product_to_schema(p) for p in products]


@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_schema(db_product)


@router.post("/products/", response_model=Product)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    db_product = crud.create_product(db=db, product_data=product_data)
    return product_to_schema(db_product)


@router.put("/products/{product_id}", response_model=Product)
def update_product(
    product_id: str,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    db_product = crud.update_product(
        db=db,
        product_id=product_id,
        product_data=product_data
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_schema(db_product)


@router.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_schema(db_product)


# =========================
# UPLOAD / LISTAGEM / REMOÇÃO DE IMAGENS
# =========================
@router.post("/products/{product_id}/images")
async def upload_product_image(
    product_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    product = crud.get_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Gera nome único com hash e salva como .webp
    file_content = await file.read()
    hash_name = hashlib.sha256(file_content).hexdigest() + ".webp"
    file_path = os.path.join(UPLOAD_DIR, hash_name)

    # Salva a imagem convertida para webp
    image = Image.open(file.file)
    image.save(file_path, format="WEBP")

    # Cria registro no banco
    new_image = ProductImage(
        product_id=product_id,
        image_url=file_path
    )
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return {
        "id": new_image.id,
        "image_url": new_image.image_url
    }


@router.get("/products/{product_id}/images")
def list_product_images(
    product_id: str,
    db: Session = Depends(get_db)
):
    product = crud.get_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Retorna todas as imagens do produto
    return [
        {
            "id": img.id,
            "image_url": img.image_url
        }
        for img in product.images
    ]


@router.delete("/products/images/{image_id}")
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

    return {"detail": "Image deleted"}
