# app/routes/customers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.database import get_db
from app.schemas.customer import Customer, CustomerCreate, CustomerUpdate


# ==============================
# Router
# ==============================
router = APIRouter(prefix="/customers", tags=["Customers"])


# =========================
# CRUD - Clientes
# =========================

# OBTER TODOS OS CLIENTES
@router.get("/", response_model=list[Customer])
def get_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    customers = crud.get_customers(db=db, skip=skip, limit=limit)
    return customers


# OBTER UM CLIENTE ESPECÍFICO
@router.get("/{customer_id}", response_model=Customer)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    db_customer = crud.get_customer(db=db, customer_id=customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


# CRIAR UM NOVO CLIENTE
@router.post("/", response_model=Customer)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    db_customer = crud.create_customer(db=db, customer_data=customer_data)
    return db_customer


# ATUALIZAR UM CLIENTE
@router.put("/{customer_id}", response_model=Customer)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    db_customer = crud.update_customer(
        db=db,
        customer_id=customer_id,
        customer_data=customer_data
    )
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


# EXCLUIR UM CLIENTE
@router.delete("/{customer_id}", response_model=Customer)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    db_customer = crud.delete_customer(db=db, customer_id=customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer
