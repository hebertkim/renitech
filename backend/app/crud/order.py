from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, OrderStatus  # Removendo OrderStatusHistory
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.models.product import Product

# =========================
# Criar pedido
# =========================
def create_order(db: Session, order: OrderCreate):
    db_order = Order(user_id=order.user_id)
    total = 0.0

    for item in order.items:
        subtotal = item.quantity * item.unit_price
        db_item = OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=subtotal,
        )
        # Atualiza estoque do produto
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock_quantity -= item.quantity
            db.add(product)
        total += subtotal
        db_order.items.append(db_item)

    db_order.total = total
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# =========================
# Atualizar status do pedido
# =========================
def update_order_status(db: Session, order_id: str, status: OrderStatusUpdate):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = status.status
        db.commit()
        db.refresh(order)
    return order

# =========================
# Deletar pedido
# =========================
def delete_order(db: Session, order_id: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
    return {"deleted": True}

# =========================
# Listar todos os pedidos
# =========================
def list_orders(db: Session):
    return db.query(Order).all()

# =========================
# Obter pedido por ID
# =========================
def get_order(db: Session, order_id: str):
    return db.query(Order).filter(Order.id == order_id).first()
