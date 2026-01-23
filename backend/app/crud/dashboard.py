from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import ProductCategory
from app.models.order import Order
from app.models.customer import Customer  # Certifique-se que Customer existe
from app.models.product import Product  # Para verificar estoque

def get_dashboard_data(db: Session):
    total_products = db.query(Product).count()
    total_categories = db.query(ProductCategory).count()
    total_orders = db.query(Order).count()
    total_customers = db.query(Customer).count()

    # Produtos com estoque abaixo do mínimo
    low_stock_products_query = db.query(Product).filter(
        Product.stock_quantity <= Product.stock_minimum
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
