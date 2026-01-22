from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import ConfigDict
from enum import Enum

# Enums compatíveis com Pydantic
class PaymentMethodEnum(str, Enum):
    cash = "CASH"
    pix = "PIX"
    ted = "TED"
    card = "CARD"
    other = "OTHER"

class ReconciliationStatusEnum(str, Enum):
    pending = "PENDING"
    reconciled = "RECONCILED"
    divergent = "DIVERGENT"

class ExpenseBase(BaseModel):
    description: str = Field(..., min_length=3, max_length=255)
    amount: Decimal = Field(..., gt=0)
    currency: Optional[str] = "BRL"
    date: datetime
    due_date: Optional[datetime] = None
    paid: Optional[bool] = False
    payment_method: Optional[PaymentMethodEnum] = PaymentMethodEnum.cash
    invoice_number: Optional[str] = None
    supplier: Optional[str] = None
    fiscal_class: Optional[str] = None
    tax_amount: Optional[Decimal] = None
    recurring: Optional[bool] = False
    recurrence_rule: Optional[dict] = None
    attachment: Optional[dict] = None
    reconciliation_status: Optional[ReconciliationStatusEnum] = ReconciliationStatusEnum.pending
    reconciliation_date: Optional[datetime] = None
    notes: Optional[str] = None
    ai_risk_flag: Optional[bool] = False
    ai_category_suggestion: Optional[str] = None
    category_id: Optional[int] = None
    account_id: Optional[int] = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
