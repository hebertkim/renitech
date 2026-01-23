from pydantic import BaseModel
from datetime import datetime

class StockCreate(BaseModel):
    product_id: str
    movement_type: str  # 'in' ou 'out'
    quantity: int

class Stock(BaseModel):
    id: str
    product_id: str
    movement_type: str
    quantity: int
    timestamp: datetime

    class Config:
        from_attributes = True  # Pydantic v2, substitui orm_mode
