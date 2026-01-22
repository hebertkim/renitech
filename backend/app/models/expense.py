from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Numeric, Boolean, Enum, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# Enum para métodos de pagamento
class PaymentMethodEnum(str, enum.Enum):
    cash = "CASH"
    pix = "PIX"
    ted = "TED"
    card = "CARD"
    other = "OTHER"

# Enum para status de conciliação
class ReconciliationStatusEnum(str, enum.Enum):
    pending = "PENDING"
    reconciled = "RECONCILED"
    divergent = "DIVERGENT"

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="BRL")
    date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=True)
    paid = Column(Boolean, default=False)
    payment_method = Column(Enum(PaymentMethodEnum), default=PaymentMethodEnum.cash)
    invoice_number = Column(String(100), nullable=True)
    supplier = Column(String(255), nullable=True)
    fiscal_class = Column(String(50), nullable=True)
    tax_amount = Column(Numeric(10, 2), nullable=True)
    recurring = Column(Boolean, default=False)
    recurrence_rule = Column(JSON, nullable=True)
    attachment = Column(JSON, nullable=True)
    reconciliation_status = Column(Enum(ReconciliationStatusEnum), default=ReconciliationStatusEnum.pending)
    reconciliation_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)  # Corrigido: Text para evitar erro no MySQL
    ai_risk_flag = Column(Boolean, default=False)
    ai_category_suggestion = Column(String(255), nullable=True)

    # Relacionamentos
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # ======================
    # ORM Relationships
    # ======================
    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
    account = relationship("Account", back_populates="expenses")
