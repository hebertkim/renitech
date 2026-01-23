from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ProductCategorySchema(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True
