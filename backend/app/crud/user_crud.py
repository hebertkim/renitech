# app/crud/user.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from passlib.hash import bcrypt
from uuid import uuid4

# =========================
# Criar usuário
# =========================
def create_user(db: Session, user_in: UserCreate, company_id: str = None, store_id: str = None) -> User:
    """
    Cria um usuário vinculado ao tenant (company_id + store_id), com senha criptografada.
    """
    hashed_password = bcrypt.hash(user_in.password)
    user = User(
        id=str(uuid4()),
        name=user_in.name,
        email=user_in.email,
        password=hashed_password,
        role=getattr(user_in, "role", "user"),
        company_id=company_id,
        store_id=store_id
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Erro ao criar usuário: {e.orig}") from e

# =========================
# Obter usuário por ID
# =========================
def get_user(db: Session, user_id: str, company_id: str = None, store_id: str = None) -> User | None:
    """
    Retorna um usuário pelo ID, filtrando pelo tenant se fornecido.
    """
    query = db.query(User).filter(User.id == user_id)
    if company_id:
        query = query.filter(User.company_id == company_id)
    if store_id:
        query = query.filter(User.store_id == store_id)
    return query.first()

# =========================
# Obter usuário por e-mail
# =========================
def get_user_by_email(db: Session, email: str, company_id: str = None, store_id: str = None) -> User | None:
    """
    Retorna um usuário pelo e-mail, filtrando pelo tenant se fornecido.
    """
    query = db.query(User).filter(User.email == email)
    if company_id:
        query = query.filter(User.company_id == company_id)
    if store_id:
        query = query.filter(User.store_id == store_id)
    return query.first()

# =========================
# Listar usuários
# =========================
def list_users(db: Session, company_id: str = None, store_id: str = None, skip: int = 0, limit: int = 100) -> list[User]:
    """
    Lista usuários do tenant, com paginação.
    """
    query = db.query(User)
    if company_id:
        query = query.filter(User.company_id == company_id)
    if store_id:
        query = query.filter(User.store_id == store_id)
    return query.offset(skip).limit(limit).all()

# =========================
# Atualizar usuário
# =========================
def update_user(db: Session, user_id: str, user_in: UserUpdate, company_id: str = None, store_id: str = None) -> User | None:
    """
    Atualiza os dados de um usuário, incluindo senha (criptografada) se fornecida.
    """
    user = get_user(db, user_id, company_id, store_id)
    if not user:
        return None

    try:
        for key, value in user_in.dict(exclude_unset=True).items():
            if key == "password":
                setattr(user, key, bcrypt.hash(value))
            else:
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao atualizar usuário: {str(e)}") from e

# =========================
# Deletar usuário
# =========================
def delete_user(db: Session, user_id: str, company_id: str = None, store_id: str = None) -> User | None:
    """
    Deleta um usuário do tenant.
    """
    user = get_user(db, user_id, company_id, store_id)
    if not user:
        return None

    try:
        db.delete(user)
        db.commit()
        return user
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao deletar usuário: {str(e)}") from e
