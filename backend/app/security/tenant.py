from fastapi import Depends, HTTPException
from app.models.user import User

class Tenant:
    def __init__(self, company_id: str, store_id: str | None):
        self.company_id = company_id
        self.store_id = store_id

def get_current_tenant(user: User = Depends(lambda: __import__('app.security').get_current_user())) -> Tenant:
    """
    Retorna o tenant (empresa + loja) do usuário logado.
    """
    if not user.company_id:
        raise HTTPException(status_code=400, detail="Usuário sem empresa atribuída")
    return Tenant(company_id=user.company_id, store_id=user.store_id)
