# app/schemas/dashboard.py
from pydantic import BaseModel
from typing import List


class LowStockProduct(BaseModel):
    product_id: str
    product_name: str
    stock_quantity: float

    class Config:
        orm_mode = True


class DashboardStats(BaseModel):
    total_products: int
    total_categories: int
    total_orders: int
    total_customers: int
    low_stock_products: int


class DashboardResponse(BaseModel):
    stats: DashboardStats
    low_stock_products: List[LowStockProduct]
