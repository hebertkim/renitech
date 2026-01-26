# app/crud/order.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.models.product import Product
from app.security.tenant import Tenant  # objeto tenant do usuário logado

# =========================
# Criar pedido
# =========================
def create_order(db: Session, order_data: OrderCreate, tenant: Tenant) -> Order:
    """
    Cria um pedido com itens e atualiza o estoque dos produtos.
    """
    db_order = Order(
        user_id=order_data.user_id,
        company_id=tenant.company_id,
        store_id=tenant.store_id,
        status="pending"  # status inicial
    )
    total = 0.0

    try:
        for item in order_data.items:
            subtotal = item.quantity * item.unit_price

            # Busca o produto e atualiza estoque
            product = db.query(Product).filter(
                Product.id == item.product_id,
                Product.company_id == tenant.company_id,
                Product.store_id == tenant.store_id,
                Product.is_active == True
            ).first()

            if not product:
                raise ValueError(f"Produto {item.product_id} não encontrado ou inativo")

            if product.stock_quantity < item.quantity:
                raise ValueError(f"Estoque insuficiente para o produto {product.name}")

            product.stock_quantity -= item.quantity
            db.add(product)

            # Cria item do pedido
            db_item = OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=subtotal,
                company_id=tenant.company_id,
                store_id=tenant.store_id
            )
            db_order.items.append(db_item)
            total += subtotal

        db_order.total = total
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    except Exception as e:
        db.rollback()
        raise e

# =========================
# Atualizar status do pedido
# =========================
def update_order_status(db: Session, order_id: str, status_data: OrderStatusUpdate, tenant: Tenant) -> Order | None:
    """
    Atualiza o status de um pedido específico.
    """
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.company_id == tenant.company_id,
        Order.store_id == tenant.store_id
    ).first()

    if order:
        order.status = status_data.status
        db.commit()
        db.refresh(order)
    return order

# =========================
# Deletar pedido
# =========================
def delete_order(db: Session, order_id: str, tenant: Tenant) -> dict:
    """
    Deleta um pedido (físico). Considerar soft delete em produção se necessário.
    """
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.company_id == tenant.company_id,
        Order.store_id == tenant.store_id
    ).first()

    if order:
        db.delete(order)
        db.commit()
        return {"deleted": True}
    return {"deleted": False, "message": "Pedido não encontrado"}

# =========================
# Listar todos os pedidos
# =========================
def list_orders(db: Session, tenant: Tenant) -> list[Order]:
    """
    Retorna todos os pedidos do tenant.
    """
    return db.query(Order).filter(
        Order.company_id == tenant.company_id,
        Order.store_id == tenant.store_id
    ).all()

# =========================
# Obter pedido por ID
# =========================
def get_order(db: Session, order_id: str, tenant: Tenant) -> Order | None:
    """
    Retorna um pedido específico pelo ID do tenant.
    """
    return db.query(Order).filter(
        Order.id == order_id,
        Order.company_id == tenant.company_id,
        Order.store_id == tenant.store_id
    ).first()
