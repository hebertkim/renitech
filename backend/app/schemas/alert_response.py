from pydantic import BaseModel
from typing import List, Literal

class AlertItem(BaseModel):
    level: Literal["info", "warning", "critical"]
    title: str
    message: str

class AlertsResponse(BaseModel):
    alerts: List[AlertItem]
    summary: str
