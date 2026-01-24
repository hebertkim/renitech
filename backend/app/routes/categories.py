# app/routes/categories.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app import crud
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
@router.post("/categories/", response_model=ProductCategory)
def create_category(
    category_data: ProductCategoryCreate,
    db: Session = Depends(get_db)
):
    return crud.create_category(db=db, category_data=category_data)


# =========================
# OBTER UMA CATEGORIA
# =========================
@router.get("/categories/{category_id}", response_model=ProductCategory)
def get_category(
    category_id: UUID,
    db: Session = Depends(get_db)
):
    db_category = crud.get_category(db=db, category_id=str(category_id))
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


# =========================
# OBTER TODAS AS CATEGORIAS
# =========================
@router.get("/categories/", response_model=List[ProductCategory])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_categories(db=db, skip=skip, limit=limit)


# =========================
# ATUALIZAR UMA CATEGORIA
# =========================
@router.put("/categories/{category_id}", response_model=ProductCategory)
def update_category(
    category_id: UUID,
    category_data: ProductCategoryUpdate,
    db: Session = Depends(get_db)
):
    db_category = crud.update_category(
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
@router.delete("/categories/{category_id}", response_model=ProductCategory)
def delete_category(
    category_id: UUID,
    db: Session = Depends(get_db)
):
    db_category = crud.delete_category(db=db, category_id=str(category_id))
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
