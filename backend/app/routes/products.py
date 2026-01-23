# app/routes/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter()

# =========================
# OBTER TODOS OS PRODUTOS
# =========================
@router.get("/products/", response_model=List[schemas.Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db=db, skip=skip, limit=limit)

# =========================
# OBTER UM PRODUTO ESPECÍFICO
# =========================
@router.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: str, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# =========================
# CRIAR UM NOVO PRODUTO
# =========================
@router.post("/products/", response_model=schemas.Product)
def create_product(product_data: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product_data=product_data)

# =========================
# ATUALIZAR UM PRODUTO
# =========================
@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: str,
    product_data: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    db_product = crud.update_product(db=db, product_id=product_id, product_data=product_data)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# =========================
# EXCLUIR UM PRODUTO
# =========================
@router.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# =========================
# NOTAS:
# - SKU já é parte do modelo Product, não é necessário endpoint separado para SKU
# - Todos os campos ERP (estoque mínimo, promoções, impostos, combos, controle de estoque)
#   estão inclusos nos schemas ProductCreate/ProductUpdate/Product
# - Suporte a imagens está pronto via campo 'images' nos schemas
