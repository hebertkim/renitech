# app/security/tenant.py

from typing import Optional
from fastapi import Depends, HTTPException
from app.models.user import User
from app.dependencies import get_current_user  # Importação unificada

class Tenant:
    """
    Representa o tenant (empresa + loja) do usuário logado.
    """
    def __init__(self, company_id: str, store_id: Optional[str] = None):
        self.company_id = company_id
        self.store_id = store_id

def get_current_tenant(user: User = Depends(get_current_user)) -> Tenant:
    """
    Retorna o tenant (empresa + loja) do usuário logado.
    Lança erro se o usuário não tiver empresa atribuída.
    """
    if not user.company_id:
        raise HTTPException(status_code=400, detail="Usuário sem empresa atribuída")
    
    return Tenant(company_id=user.company_id, store_id=user.store_id)
