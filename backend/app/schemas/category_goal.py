from pydantic import BaseModel
from datetime import date

class CategoryGoalBase(BaseModel):
    category_id: int
    target_amount: float
    month: int
    year: int

class CategoryGoalCreate(CategoryGoalBase):
    pass

class CategoryGoalResponse(CategoryGoalBase):
    id: int

    class Config:
        from_attributes = True
