# app/middleware/tenant.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Pega company_id e store_id do header (ou default)
        company_id = request.headers.get("X-Company-ID")
        store_id = request.headers.get("X-Store-ID")
        request.state.company_id = company_id
        request.state.store_id = store_id
        response = await call_next(request)
        return response
