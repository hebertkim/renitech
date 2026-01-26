from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from passlib.hash import bcrypt
from uuid import uuid4

# =========================
# Criar usuário
# =========================
def create_user(db: Session, user_in: UserCreate, company_id: str = None, store_id: str = None) -> User:
    hashed_password = bcrypt.hash(user_in.password)
    user = User(
        id=str(uuid4()),
        name=user_in.name,
        email=user_in.email,
        password=hashed_password,
        role=user_in.role if hasattr(user_in, "role") else "user",
        company_id=company_id,
        store_id=store_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# =========================
# Obter usuário por ID
# =========================
def get_user(db: Session, user_id: str, company_id: str = None, store_id: str = None):
    query = db.query(User).filter(User.id == user_id)
    if company_id:
        query = query.filter(User.company_id == company_id)
    if store_id:
        query = query.filter(User.store_id == store_id)
    return query.first()

# =========================
# Obter usuário por e-mail
# =========================
def get_user_by_email(db: Session, email: str, company_id: str = None, store_id: str = None):
    query = db.query(User).filter(User.email == email)
    if company_id:
        query = query.filter(User.company_id == company_id)
    if store_id:
        query = query.filter(User.store_id == store_id)
    return query.first()

# =========================
# Listar usuários
# =========================
def list_users(db: Session, company_id: str = None, store_id: str = None, skip: int = 0, limit: int = 100):
    query = db.query(User)
    if company_id:
        query = query.filter(User.company_id == company_id)
    if store_id:
        query = query.filter(User.store_id == store_id)
    return query.offset(skip).limit(limit).all()

# =========================
# Atualizar usuário
# =========================
def update_user(db: Session, user_id: str, user_in: UserUpdate, company_id: str = None, store_id: str = None):
    user = get_user(db, user_id, company_id, store_id)
    if not user:
        return None

    for key, value in user_in.dict(exclude_unset=True).items():
        if key == "password":
            setattr(user, key, bcrypt.hash(value))
        else:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# =========================
# Deletar usuário
# =========================
def delete_user(db: Session, user_id: str, company_id: str = None, store_id: str = None):
    user = get_user(db, user_id, company_id, store_id)
    if user:
        db.delete(user)
        db.commit()
    return user
