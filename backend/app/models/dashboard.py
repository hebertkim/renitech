# app/models/dashboard.py
from sqlalchemy.orm import Session
from app.models.product import Product, ProductCategory
from app.models.order import Order
from app.models.customer import Customer


# =========================
# Função para coletar os dados do Dashboard
# =========================
def get_dashboard_data(db: Session, company_id: str | None = None, store_id: str | None = None):
    """
    Retorna dados agregados para o dashboard:
    - total de produtos
    - total de categorias
    - total de pedidos
    - total de clientes
    - produtos com estoque baixo
    """

    # =========================
    # Filtros multi-tenant
    # =========================
    tenant_filters = lambda model: [
        *( [model.company_id == company_id] if company_id else [] ),
        *( [model.store_id == store_id] if store_id else [] )
    ]

    # =========================
    # Total de produtos
    # =========================
    total_products = db.query(Product).filter(*tenant_filters(Product)).count()

    # =========================
    # Total de categorias
    # =========================
    total_categories = db.query(ProductCategory).filter(*tenant_filters(ProductCategory)).count()

    # =========================
    # Total de pedidos
    # =========================
    total_orders = db.query(Order).filter(*tenant_filters(Order)).count()

    # =========================
    # Total de clientes
    # =========================
    total_customers = db.query(Customer).filter(*tenant_filters(Customer)).count()

    # =========================
    # Produtos com estoque baixo
    # =========================
    low_stock_products = (
        db.query(Product)
        .filter(Product.stock_quantity <= Product.stock_minimum, Product.is_active == True, *tenant_filters(Product))
        .all()
    )

    # =========================
    # Retorno padronizado
    # =========================
    return {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "low_stock_products": [p.to_dict() for p in low_stock_products],
    }
