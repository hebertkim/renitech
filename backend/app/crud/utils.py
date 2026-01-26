# app/crud/utils.py
from sqlalchemy.orm import Query
from app.security.tenant import Tenant
from typing import Type

def apply_tenant_filter(query: Query, model: Type, tenant: Tenant) -> Query:
    """
    Aplica filtro multi-tenant em qualquer query.

    Args:
        query (Query): Query SQLAlchemy a ser filtrada.
        model (Type): Modelo SQLAlchemy que contém company_id e opcionalmente store_id.
        tenant (Tenant): Tenant do usuário logado (company_id + store_id).

    Returns:
        Query: Query filtrada pelo tenant.
    """
    filters = [model.company_id == tenant.company_id]

    # Aplica store_id se o modelo tiver este atributo e tenant.store_id existir
    if hasattr(model, "store_id") and tenant.store_id:
        filters.append(model.store_id == tenant.store_id)

    return query.filter(*filters)
