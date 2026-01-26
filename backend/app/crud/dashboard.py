# app/crud/dashboard.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import Product
from app.models.category import ProductCategory
from app.models.order import Order
from app.models.customer import Customer
from app.security.tenant import Tenant  # nosso objeto tenant

def get_dashboard_data(db: Session, tenant: Tenant):
    """
    Retorna estatísticas do dashboard filtradas por tenant (company_id e store_id),
    de forma otimizada e segura para produção.
    """
    # ----------------------
    # Filtros multi-tenant
    # ----------------------
    product_filter = [Product.company_id == tenant.company_id, Product.is_active == True]
    category_filter = [ProductCategory.company_id == tenant.company_id, ProductCategory.is_active == True]
    order_filter = [Order.company_id == tenant.company_id]
    customer_filter = [Customer.company_id == tenant.company_id]

    if tenant.store_id:
        product_filter.append(Product.store_id == tenant.store_id)
        category_filter.append(ProductCategory.store_id == tenant.store_id)
        order_filter.append(Order.store_id == tenant.store_id)
        customer_filter.append(Customer.store_id == tenant.store_id)

    # ----------------------
    # Totais
    # ----------------------
    total_products = db.query(func.count(Product.id)).filter(*product_filter).scalar()
    total_categories = db.query(func.count(ProductCategory.id)).filter(*category_filter).scalar()
    total_orders = db.query(func.count(Order.id)).filter(*order_filter).scalar()
    total_customers = db.query(func.count(Customer.id)).filter(*customer_filter).scalar()

    # ----------------------
    # Produtos com estoque baixo
    # ----------------------
    low_stock_products_query = (
        db.query(Product.id, Product.name, Product.stock_quantity)
        .filter(Product.stock_quantity <= Product.stock_minimum, *product_filter)
        .all()
    )

    low_stock_products = [
        {
            "product_id": p.id,
            "product_name": p.name,
            "stock_quantity": p.stock_quantity
        }
        for p in low_stock_products_query
    ]

    # ----------------------
    # Montando retorno
    # ----------------------
    stats = {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "low_stock_products": len(low_stock_products)
    }

    return {
        "stats": stats,
        "low_stock_products": low_stock_products
    }
