from pydantic import BaseModel
from datetime import date
from typing import List

class MissionBase(BaseModel):
    title: str
    description: str
    type: str
    difficulty: str
    reward_points: int
    start_date: date
    end_date: date
    progress: float
    completed: bool

class MissionResponse(MissionBase):
    id: int

    class Config:
        from_attributes = True

class MissionsListResponse(BaseModel):
    missions: List[MissionResponse]
