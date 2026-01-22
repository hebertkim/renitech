from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.alert_service import detect_expense_anomalies
from app.crud.alert_crud import get_alerts
from app.schemas.alert import Alert as AlertSchema

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/", response_model=list[AlertSchema])
def read_alerts(user_id: int, db: Session = Depends(get_db)):
    return get_alerts(db, user_id)

@router.post("/detect", response_model=list[AlertSchema])
def run_alerts_detection(user_id: int, db: Session = Depends(get_db)):
    return detect_expense_anomalies(db, user_id)
