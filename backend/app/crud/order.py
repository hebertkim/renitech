# app/crud/order.py
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product, StockMovement, StockMovementType

# =========================
# Criar pedido
# =========================
def create_order(db: Session, user_id: str, items: list):
    total = 0.0
    order_items = []

    for item in items:
        product = db.query(Product).filter(Product.id == item['product_id']).first()
        if not product:
            raise Exception(f"Produto {item['product_id']} não encontrado")

        if product.stock_quantity < item['quantity']:
            raise Exception(f"Estoque insuficiente para o produto {product.id}")

        subtotal = item['quantity'] * product.price
        total += subtotal

        # Cria item do pedido
        order_item = OrderItem(
            product_id=product.id,
            quantity=item['quantity'],
            unit_price=product.price,
            subtotal=subtotal
        )
        order_items.append(order_item)

        # Baixa automática do estoque
        product.stock_quantity -= item['quantity']

        # Registra movimento de estoque
        stock_movement = StockMovement(
            product_id=product.id,
            quantity=item['quantity'],
            movement_type=StockMovementType.OUT
        )
        db.add(stock_movement)

    # Cria pedido
    order = Order(
        user_id=user_id,
        total=total,
        items=order_items
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

# =========================
# Atualizar status do pedido
# =========================
def update_order_status(db: Session, order_id: str, status: OrderStatus):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise Exception("Pedido não encontrado")

    order.status = status
    db.commit()
    db.refresh(order)
    return order

# =========================
# Deletar pedido
# =========================
def delete_order(db: Session, order_id: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise Exception("Pedido não encontrado")
    
    # Restituir estoque
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock_quantity += item.quantity
            # Movimento de estoque de retorno
            stock_movement = StockMovement(
                product_id=product.id,
                quantity=item.quantity,
                movement_type=StockMovementType.IN
            )
            db.add(stock_movement)
    
    db.delete(order)
    db.commit()
    return True

# =========================
# Listar pedidos
# =========================
def list_orders(db: Session):
    return db.query(Order).all()

# =========================
# Obter pedido por ID
# =========================
def get_order(db: Session, order_id: str):
    return db.query(Order).filter(Order.id == order_id).first()
