from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import SessionLocal
from app.security import create_access_token, authenticate_user
from app.models.user import User
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas para login
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

# =========================
# Login Route (POST /auth/login)
# =========================
@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # Autenticando o usuário
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gerando o token JWT
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)

    return LoginResponse(access_token=access_token, token_type="bearer")

# =========================
# Logout Route (POST /auth/logout)
# =========================
@router.post("/logout")
def logout():
    # O logout em sistemas baseados em JWT geralmente não requer um processamento do lado do servidor,
    # pois o JWT não é armazenado no servidor. O que você pode fazer é pedir para o cliente "descartar" o token.
    # Caso precise de uma lista de tokens revogados, seria necessário um banco de dados para armazenar o estado.
    return {"detail": "Logout bem-sucedido"}
