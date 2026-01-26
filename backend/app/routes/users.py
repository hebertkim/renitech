# app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from PIL import Image
import hashlib
import io
import os

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate, Token

# ✅ AUTH E PERMISSÕES CENTRALIZADAS
from app.dependencies import (
    get_current_user,
    require_admin,
    require_superadmin,
)

# ==============================
# Router
# ==============================
router = APIRouter(prefix="/users", tags=["Users"])

# ==============================
# Password hashing
# ==============================
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ==============================
# JWT configuration
# ==============================
SECRET_KEY = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ==============================
# DIRETÓRIO REAL DE UPLOAD
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVATAR_DIR = os.path.join(BASE_DIR, "assets", "img", "profile")
os.makedirs(AVATAR_DIR, exist_ok=True)

MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB
AVATAR_MAX_DIM = (512, 512)

# ==============================
# CRIAR USUÁRIO (PUBLICO)
# ==============================
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    hashed_password = hash_password(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role="cliente",  # 👈 SEMPRE CLIENTE POR PADRÃO
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# ==============================
# LOGIN
# ==============================
@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...),
):
    user = db.query(User).filter(User.email == username).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role,
        }
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ==============================
# CURRENT USER
# ==============================
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_update.name is not None:
        current_user.name = user_update.name

    if user_update.email is not None:
        current_user.email = user_update.email

    if user_update.password:
        current_user.password = hash_password(user_update.password)

    db.commit()
    db.refresh(current_user)

    return current_user


# ==============================
# UPLOAD DE AVATAR
# ==============================
@router.post("/me/avatar", response_model=UserResponse)
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = file.file.read()

    if len(content) > MAX_AVATAR_SIZE:
        raise HTTPException(status_code=400, detail="Arquivo muito grande. Máx 5MB.")

    try:
        image = Image.open(io.BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem válida.")

    image.thumbnail(AVATAR_MAX_DIM)

    # Remove avatar antigo
    if current_user.avatar:
        old_path = os.path.join(BASE_DIR, current_user.avatar.lstrip("/"))
        if os.path.exists(old_path):
            os.remove(old_path)

    # Hash único
    file_hash = hashlib.sha256(
        (str(current_user.id) + file.filename + str(datetime.utcnow())).encode()
    ).hexdigest()

    filename = f"{file_hash}.webp"
    file_path = os.path.join(AVATAR_DIR, filename)

    image.save(file_path, "WEBP", quality=90)

    avatar_url = f"/assets/img/profile/{filename}"
    current_user.avatar = avatar_url

    db.commit()
    db.refresh(current_user)

    return current_user


# ==============================
# ADMIN AREA
# ==============================

# 🔒 Lista todos usuários (admin ou superadmin)
@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return db.query(User).all()


# 🔒 Busca usuário por ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user


# ==============================
# SUPERADMIN ONLY (futuro)
# ==============================

# Exemplo futuro:
# - Criar admin
# - Mudar role
# - Banir usuário
# - etc
#
# @router.put("/{user_id}/role")
# def update_user_role(...):
#     ...
