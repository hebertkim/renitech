# app/routes/products.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app import crud
from app.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    Product,
    product_to_schema
)
from app.models.product_image import ProductImage
from app.models.user import User

# ✅ PADRÃO ÚNICO DE AUTH
from app.security import get_current_user

import os
import hashlib
from PIL import Image
from io import BytesIO

# ==============================
# Uploads
# ==============================
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_IMAGE_TYPES = ["JPEG", "PNG", "WEBP"]  # 🔒 opcional para segurança
MAX_IMAGE_SIZE_MB = 5

# ==============================
# Router
# ==============================
router = APIRouter(prefix="/products", tags=["Products"])

# ==============================
# DEPENDÊNCIA DE PERMISSÃO
# ==============================
def require_admin(user: User = Depends(get_current_user)):
    if user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user

# ==============================
# PRODUTOS (ROTAS PROTEGIDAS)
# ==============================
@router.get("/", response_model=List[Product])
def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    products = crud.get_products(db=db, skip=skip, limit=limit)
    return [product_to_schema(p) for p in products]


@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_product = crud.get_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_schema(db_product)

# ==============================
# PRODUTOS (ROTAS ADMIN)
# ==============================
@router.post("/", response_model=Product)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    db_product = crud.create_product(db=db, product_data=product_data)
    return product_to_schema(db_product)


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: str,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    db_product = crud.update_product(db=db, product_id=product_id, product_data=product_data)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_schema(db_product)


@router.delete("/{product_id}", response_model=Product)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    db_product = crud.delete_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_schema(db_product)

# ==============================
# IMAGENS (ROTAS ADMIN)
# ==============================
@router.post("/{product_id}/images")
async def upload_product_image(
    product_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    product = crud.get_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    file_content = await file.read()

    # 🔒 Validação tamanho máximo
    if len(file_content) > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"Arquivo muito grande. Máx {MAX_IMAGE_SIZE_MB}MB.")

    # 🔒 Validação de imagem
    try:
        image = Image.open(BytesIO(file_content))
        image.verify()
        image = Image.open(BytesIO(file_content))  # reabrir após verify
        if image.format not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Tipo de imagem não permitido")
    except Exception:
        raise HTTPException(status_code=400, detail="Arquivo de imagem inválido")

    # Hash único
    hash_name = hashlib.sha256(file_content).hexdigest() + ".webp"
    product_dir = os.path.join(UPLOAD_DIR, product_id)
    os.makedirs(product_dir, exist_ok=True)
    file_path = os.path.join(product_dir, hash_name)

    # Salva imagem
    image.save(file_path, format="WEBP")

    # URL relativa para frontend
    image_url = f"/{UPLOAD_DIR}/{product_id}/{hash_name}"

    new_image = ProductImage(
        product_id=product_id,
        image_url=image_url
    )
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return {
        "id": new_image.id,
        "image_url": new_image.image_url
    }


@router.get("/{product_id}/images")
def list_product_images(
    product_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    product = crud.get_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return [
        {"id": img.id, "image_url": img.image_url}
        for img in product.images
    ]


@router.delete("/images/{image_id}")
def delete_product_image(
    image_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Remove arquivo físico
    if os.path.exists(image.image_url.lstrip("/")):  # ajusta para path relativo
        os.remove(image.image_url.lstrip("/"))

    db.delete(image)
    db.commit()

    return {"detail": "Image deleted"}
