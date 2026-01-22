from pydantic import BaseModel
from datetime import date

class AlertBase(BaseModel):
    user_id: int
    category_id: int
    tipo: str
    mensagem: str
    valor: float
    threshold: float
    data: date

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    class Config:
        from_attributes = True
