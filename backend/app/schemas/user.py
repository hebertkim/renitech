# app/schemas/user.py

from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional
from datetime import datetime
from uuid import UUID

# ============================
# --- Schemas base ---
# ============================


class UserBase(BaseModel):
    name: str
    email: EmailStr


# ============================
# Schema para criação de usuário
# ============================
class UserCreate(UserBase):
    password: str  # Somente no create
    confirm_password: str  # Para validação no backend

    # ✅ Validação para garantir que as senhas correspondem (Pydantic v2)
    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


# ============================
# Schema para atualizar os dados do usuário
# ============================
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    # ✅ Avatar é opcional
    avatar: Optional[str] = None


# ============================
# --- Schema de resposta ---
# ============================
class UserResponse(UserBase):
    id: UUID
    balance: float
    created_at: datetime

    # ✅ Avatar opcional
    avatar: Optional[str] = None

    # ✅ Pydantic v2 replacement for orm_mode
    model_config = {
        "from_attributes": True
    }


# ============================
# --- JWT Token ---
# ============================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
