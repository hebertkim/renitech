# app/routes/profile.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

# ✅ Auth centralizada
from app.dependencies import get_current_user
from app.routes.users import hash_password  # reutiliza a função existente

# ==============================
# Router
# ==============================
router = APIRouter(prefix="/profiles", tags=["Profiles"])

# ==============================
# OBTER MEU PERFIL
# ==============================
@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Retorna os dados do usuário atualmente autenticado.
    """
    return current_user


# ==============================
# ATUALIZAR MEU PERFIL
# ==============================
@router.put("/me", response_model=UserResponse)
def update_my_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Atualiza nome, e-mail, senha ou avatar do usuário autenticado.
    Valida se o e-mail informado já existe no sistema.
    """
    if data.name is not None:
        current_user.name = data.name

    if data.email is not None:
        # Verifica se email já existe em outro usuário
        existing_user = db.query(User).filter(
            User.email == data.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="E-mail já está em uso")
        current_user.email = data.email

    if data.avatar is not None:
        current_user.avatar = data.avatar

    if data.password:
        current_user.password = hash_password(data.password)

    db.commit()
    db.refresh(current_user)

    return current_user
