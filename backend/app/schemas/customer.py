# app/schemas/customer.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# =========================
# Base do Cliente
# =========================
class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

# =========================
# Modelo para criação
# =========================
class CustomerCreate(CustomerBase):
    pass

# =========================
# Modelo para atualização
# =========================
class CustomerUpdate(CustomerBase):
    pass

# =========================
# Modelo de leitura
# =========================
class Customer(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
