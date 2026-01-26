# app/routes/categories.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

# CRUD
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
from app.models.user import User
from app.security import get_current_user

# ==============================
# Router
# ==============================
router = APIRouter(prefix="/categories", tags=["Categories"])

# ==============================
# DEPENDÊNCIAS DE PERMISSÃO
# ==============================
def require_admin(user: User = Depends(get_current_user)):
    """Permite acesso apenas a admins e superadmins"""
    if user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user

# =========================
# ROTAS PÚBLICAS
# =========================

@router.get("/{category_id}", response_model=ProductCategory)
def get_category_endpoint(
    category_id: UUID,
    db: Session = Depends(get_db)
):
    """Obter uma categoria específica (público)"""
    db_category = get_category(db=db, category_id=str(category_id))
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.get("/", response_model=List[ProductCategory])
def list_categories_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar todas as categorias (público)"""
    return get_categories(db=db, skip=skip, limit=limit)

# =========================
# ROTAS ADMIN
# =========================

@router.post("/", response_model=ProductCategory)
def create_category_endpoint(
    category_data: ProductCategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    """Criar uma nova categoria"""
    return create_category(db=db, category_data=category_data)

@router.put("/{category_id}", response_model=ProductCategory)
def update_category_endpoint(
    category_id: UUID,
    category_data: ProductCategoryUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    """Atualizar uma categoria existente"""
    db_category = update_category(
        db=db,
        category_id=str(category_id),
        category_data=category_data
    )
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/{category_id}", response_model=ProductCategory)
def delete_category_endpoint(
    category_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    """Excluir uma categoria"""
    db_category = delete_category(db=db, category_id=str(category_id))
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
