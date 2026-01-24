# app/models/dashboard.py
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import ProductCategory
from app.models.order import Order
# Certifique-se de que o modelo de cliente existe
from app.models.customer import Customer


# Função para coletar os dados do Dashboard
def get_dashboard_data(db: Session):
    # Total de produtos
    total_products = db.query(Product).count()

    # Total de categorias
    total_categories = db.query(ProductCategory).count()

    # Total de pedidos
    total_orders = db.query(Order).count()

    # Total de clientes
    total_customers = db.query(Customer).count()

    # Produtos com estoque baixo (abaixo do estoque mínimo)
    low_stock_products = (
        db.query(Product)
        .filter(Product.stock_quantity <= Product.stock_minimum)
        .all()
    )

    return {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "low_stock_products": low_stock_products,
    }
