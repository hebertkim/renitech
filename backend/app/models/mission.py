from sqlalchemy import Column, Integer, String, Date, Boolean, Float
from app.database import Base

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(500))
    type = Column(String(50))  # habit, saving, discipline, goal, challenge
    difficulty = Column(String(20))  # easy, medium, hard
    reward_points = Column(Integer, default=0)

    start_date = Column(Date)
    end_date = Column(Date)

    progress = Column(Float, default=0)  # 0–100
    completed = Column(Boolean, default=False)
