from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.mission_service import MissionService
from app.schemas.mission import MissionsListResponse

router = APIRouter(prefix="/missions", tags=["Missions"])

@router.get("/", response_model=MissionsListResponse)
def get_missions(db: Session = Depends(get_db)):
    missions = MissionService.list_missions(db)
    return {"missions": missions}
