# app/middleware/tenant.py
from fastapi import Request
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import get_db
from app.models.user import User
from fastapi import Depends

class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware para injetar company_id e store_id
    em requests, permitindo queries multi-tenant.
    """

    async def dispatch(self, request: Request, call_next):
        # Pegamos o DB da request (usando dependência do FastAPI)
        request.state.db: Session = request.scope.get("db")
        request.state.company_id = None
        request.state.store_id = None

        # Se houver usuário logado, definimos tenant
        user: User = request.scope.get("current_user")
        if user:
            request.state.company_id = getattr(user, "company_id", None)
            request.state.store_id = getattr(user, "store_id", None)

        response = await call_next(request)
        return response
