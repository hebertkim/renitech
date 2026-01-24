# app/routes/categories.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

# IMPORTAR CRUD CORRETAMENTE DO SUBMÓDULO category
from app.crud.category import (
    create_category,
    get_category,
    get_categories,
    update_category,
    delete_category
)

from app.schemas.category import (
    ProductCategory,
    ProductCategoryCreate,
    ProductCategoryUpdate
)
from app.database import get_db

# ==============================
# Router
# ==============================
router = APIRouter(prefix="/categories", tags=["Categories"])

# =========================
# CRIAR CATEGORIA
# =========================
@router.post("/", response_model=ProductCategory)
def create_category_endpoint(
    category_data: ProductCategoryCreate,
    db: Session = Depends(get_db)
):
    return create_category(db=db, category_data=category_data)


# =========================
# OBTER UMA CATEGORIA
# =========================
@router.get("/{category_id}", response_model=ProductCategory)
def get_category_endpoint(
    category_id: UUID,
    db: Session = Depends(get_db)
):
    db_category = get_category(db=db, category_id=str(category_id))
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


# =========================
# OBTER TODAS AS CATEGORIAS
# =========================
@router.get("/", response_model=List[ProductCategory])
def list_categories_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_categories(db=db, skip=skip, limit=limit)


# =========================
# ATUALIZAR UMA CATEGORIA
# =========================
@router.put("/{category_id}", response_model=ProductCategory)
def update_category_endpoint(
    category_id: UUID,
    category_data: ProductCategoryUpdate,
    db: Session = Depends(get_db)
):
    db_category = update_category(
        db=db,
        category_id=str(category_id),
        category_data=category_data
    )
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


# =========================
# EXCLUIR UMA CATEGORIA
# =========================
@router.delete("/{category_id}", response_model=ProductCategory)
def delete_category_endpoint(
    category_id: UUID,
    db: Session = Depends(get_db)
):
    db_category = delete_category(db=db, category_id=str(category_id))
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
