from fastapi import UploadFile, File
import hashlib
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate, Token
import os
from PIL import Image
import io

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ==============================
# Dependency: Get current user
# ==============================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user

# ==============================
# DIRETÓRIO REAL DE UPLOAD
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVATAR_DIR = os.path.join(BASE_DIR, "assets", "img", "profile")
os.makedirs(AVATAR_DIR, exist_ok=True)

MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_TYPES = ["jpeg", "png", "gif", "bmp", "webp"]
AVATAR_MAX_DIM = (512, 512)  # Redimensionar para no máximo 512x512

# ==============================
# CRUD
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
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

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
# UPLOAD DE AVATAR COM REDIMENSIONAMENTO E WEBP
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

    # Redimensiona mantendo proporção
    image.thumbnail(AVATAR_MAX_DIM)

    # Deleta avatar antigo se existir
    if current_user.avatar:
        old_path = os.path.join(BASE_DIR, current_user.avatar.lstrip("/"))
        if os.path.exists(old_path):
            os.remove(old_path)

    # Hash único
    file_hash = hashlib.sha256(
        (str(current_user.id) + file.filename + str(datetime.utcnow())).encode()
    ).hexdigest()

    # Salva em WebP
    filename = f"{file_hash}.webp"
    file_path = os.path.join(AVATAR_DIR, filename)
    image.save(file_path, "WEBP", quality=90)

    avatar_url = f"/assets/img/profile/{filename}"
    current_user.avatar = avatar_url
    db.commit()
    db.refresh(current_user)

    return current_user

# ==============================
# BY ID
# ==============================
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

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

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
