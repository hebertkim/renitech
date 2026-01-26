# app/routes/customers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.database import get_db
from app.schemas.customer import Customer, CustomerCreate, CustomerUpdate
from app.models.user import User
from app.security import get_current_user

# ==============================
# Router
# ==============================
router = APIRouter(prefix="/customers", tags=["Customers"])

# ==============================
# DEPENDÊNCIAS DE PERMISSÃO
# ==============================
def require_staff(user: User = Depends(get_current_user)):
    """Permite acesso a vendedores, admins e superadmins"""
    if user.role not in ["vendedor", "admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user

def require_admin(user: User = Depends(get_current_user)):
    """Permite acesso apenas a admins e superadmins"""
    if user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user

# =========================
# CRUD - Clientes
# =========================

# OBTER TODOS OS CLIENTES (STAFF)
@router.get("/", response_model=list[Customer])
def get_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),
):
    return crud.get_customers(db=db, skip=skip, limit=limit)

# OBTER UM CLIENTE ESPECÍFICO (STAFF)
@router.get("/{customer_id}", response_model=Customer)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),
):
    db_customer = crud.get_customer(db=db, customer_id=customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# CRIAR UM NOVO CLIENTE (STAFF)
@router.post("/", response_model=Customer)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),
):
    return crud.create_customer(db=db, customer_data=customer_data)

# ATUALIZAR UM CLIENTE (STAFF)
@router.put("/{customer_id}", response_model=Customer)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),
):
    db_customer = crud.update_customer(
        db=db,
        customer_id=customer_id,
        customer_data=customer_data
    )
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# EXCLUIR UM CLIENTE (ADMIN)
@router.delete("/{customer_id}", response_model=Customer)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    db_customer = crud.delete_customer(db=db, customer_id=customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer
