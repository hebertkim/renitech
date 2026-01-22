# app/models/alert_history.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base

class AlertHistory(Base):
    __tablename__ = "alert_history"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    level = Column(String(50), nullable=False)  # info / warning / critical
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
