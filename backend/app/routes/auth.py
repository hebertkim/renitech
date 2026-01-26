# app/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import timedelta
from app.database import get_db
from app.security import create_access_token, authenticate_user
from app.models.user import User

# ==============================
# Router
# ==============================
router = APIRouter(prefix="/auth", tags=["Authentication"])

# ==============================
# Pydantic Schemas
# ==============================
class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str

# ==============================
# Login Endpoint
# ==============================
@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica o usuário e retorna um token JWT.
    """
    user: User | None = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Tempo de expiração do token
    access_token_expires = timedelta(minutes=60)

    # Gera o token JWT incluindo o role do usuário
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )

    return LoginResponse(access_token=access_token, token_type="bearer")

# ==============================
# Logout Endpoint
# ==============================
@router.post("/logout")
def logout():
    """
    Logout JWT — no backend não há processamento,
    basta o cliente descartar o token.
    """
    return {"detail": "Logout bem-sucedido"}
