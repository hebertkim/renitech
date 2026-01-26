# backend/app/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import get_db
from app.models.user import User

# ====== Config JWT ======
# ⚠️ Em produção, isso DEVE vir de variável de ambiente
SECRET_KEY = "sua_chave_secreta_aqui"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# =========================
# Função para pegar o usuário logado
# =========================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")  # "sub" = subject (id do usuário)

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    # ⚠️ CORREÇÃO: seu ID é UUID/string, NÃO int
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
        )

    return user


# =========================
# Dependências de permissão por role
# =========================

def require_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Apenas garante que o usuário está autenticado
    """
    return current_user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Apenas admin ou superadmin
    """
    if current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente",
        )
    return current_user


def require_superadmin(current_user: User = Depends(get_current_user)) -> User:
    """
    Apenas superadmin
    """
    if current_user.role != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente",
        )
    return current_user
