from sqlalchemy.orm import Session
from app.models.alert import Alert

def get_alerts(db: Session, user_id: int):
    return db.query(Alert).filter(Alert.user_id == user_id).all()
