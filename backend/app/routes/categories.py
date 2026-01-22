from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import re
import uuid

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.routes.users import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# ----------------------
# VALIDAR NOME
# ----------------------
def validate_name(db: Session, name: str, exclude_id: Optional[uuid.UUID] = None):
    name = name.strip().title()

    if not re.match(r'^[\w\sÀ-ÿ\-]+$', name):
        raise HTTPException(status_code=400, detail="Nome inválido")

    q = db.query(Category).filter(Category.name.ilike(name))
    if exclude_id:
        q = q.filter(Category.id != str(exclude_id))

    if q.first():
        raise HTTPException(status_code=400, detail="Categoria já existe")

    return name

# =========================
# CREATE
# =========================
@router.post("/", response_model=CategoryOut)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    name = validate_name(db, data.name)

    cat = Category(
        name=name,
        type=data.type,
        parent_id=str(data.parent_id) if data.parent_id else None,
        description=data.description,
        fiscal_class=data.fiscal_class,
        ai_rules=data.ai_rules
    )

    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

# =========================
# LIST
# =========================
@router.get("/", response_model=List[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Category).order_by(Category.type, Category.name).all()

# =========================
# GET BY ID
# =========================
@router.get("/{category_id}", response_model=CategoryOut)
def get_category(
    category_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cat = db.query(Category).filter(Category.id == str(category_id)).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return cat

# =========================
# UPDATE
# =========================
@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: uuid.UUID,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cat = db.query(Category).filter(Category.id == str(category_id)).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    if data.name is not None:
        cat.name = validate_name(db, data.name, exclude_id=category_id)

    if data.type is not None:
        cat.type = data.type

    if data.parent_id is not None:
        cat.parent_id = str(data.parent_id)

    if data.description is not None:
        cat.description = data.description

    if data.fiscal_class is not None:
        cat.fiscal_class = data.fiscal_class

    if data.ai_rules is not None:
        cat.ai_rules = data.ai_rules

    db.commit()
    db.refresh(cat)
    return cat

# =========================
# DELETE
# =========================
@router.delete("/{category_id}", response_model=dict)
def delete_category(
    category_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cat = db.query(Category).filter(Category.id == str(category_id)).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    # Verificando se há despesas ou receitas associadas
    if cat.expenses or cat.incomes:
        raise HTTPException(
            status_code=400,
            detail="Categoria possui lançamentos associados e não pode ser deletada"
        )

    db.delete(cat)
    db.commit()
    return {"detail": "Categoria deletada com sucesso"}
