# app/models/dashboard.py
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.product import ProductCategory
from app.models.order import Order
from app.models.customer import Customer


# Função para coletar os dados do Dashboard
def get_dashboard_data(db: Session, company_id: str | None = None, store_id: str | None = None):
    query_filter = []
    if company_id:
        query_filter.append(Product.company_id == company_id)
    if store_id:
        query_filter.append(Product.store_id == store_id)

    # Total de produtos
    total_products = db.query(Product).filter(*query_filter).count()

    # Total de categorias
    total_categories = db.query(ProductCategory).count()  # Categories podem ser globais ou multi-tenant depois

    # Total de pedidos
    order_filter = []
    if company_id:
        order_filter.append(Order.company_id == company_id)
    if store_id:
        order_filter.append(Order.store_id == store_id)
    total_orders = db.query(Order).filter(*order_filter).count()

    # Total de clientes
    customer_filter = []
    if company_id:
        customer_filter.append(Customer.company_id == company_id)
    if store_id:
        customer_filter.append(Customer.store_id == store_id)
    total_customers = db.query(Customer).filter(*customer_filter).count()

    # Produtos com estoque baixo (abaixo do estoque mínimo)
    low_stock_products = (
        db.query(Product)
        .filter(Product.stock_quantity <= Product.stock_minimum, *query_filter)
        .all()
    )

    return {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "low_stock_products": low_stock_products,
    }
