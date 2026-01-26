from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import ProductCategory
from app.models.order import Order
from app.models.customer import Customer
from app.security.tenant import Tenant  # nosso objeto tenant

def get_dashboard_data(db: Session, tenant: Tenant):
    """
    Retorna estatísticas do dashboard filtradas por tenant (company_id e store_id).
    """
    # Filtros padrão multi-tenant
    product_filter = [Product.company_id == tenant.company_id]
    category_filter = [ProductCategory.company_id == tenant.company_id]
    order_filter = [Order.company_id == tenant.company_id]
    customer_filter = [Customer.company_id == tenant.company_id]

    if tenant.store_id:
        product_filter.append(Product.store_id == tenant.store_id)
        category_filter.append(ProductCategory.store_id == tenant.store_id)
        order_filter.append(Order.store_id == tenant.store_id)
        customer_filter.append(Customer.store_id == tenant.store_id)

    # Totais
    total_products = db.query(Product).filter(*product_filter).count()
    total_categories = db.query(ProductCategory).filter(*category_filter).count()
    total_orders = db.query(Order).filter(*order_filter).count()
    total_customers = db.query(Customer).filter(*customer_filter).count()

    # Produtos com estoque abaixo do mínimo
    low_stock_products_query = db.query(Product).filter(
        Product.stock_quantity <= Product.stock_minimum,
        *product_filter
    ).all()

    low_stock_products = [
        {
            "product_id": p.id,
            "product_name": p.name,
            "stock_quantity": p.stock_quantity
        } for p in low_stock_products_query
    ]

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
