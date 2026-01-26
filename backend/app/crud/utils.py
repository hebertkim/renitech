# app/crud/utils.py
from sqlalchemy.orm import Query
from app.security.tenant import Tenant

def apply_tenant_filter(query: Query, model, tenant: Tenant):
    """
    Aplica filtro por company_id e store_id em qualquer query.
    """
    filters = [model.company_id == tenant.company_id]
    if hasattr(model, "store_id") and tenant.store_id:
        filters.append(model.store_id == tenant.store_id)
    return query.filter(*filters)
