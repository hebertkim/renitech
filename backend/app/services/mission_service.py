from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.models.mission import Mission
from app.models.expense import Expense

class MissionService:

    @staticmethod
    def generate_default_missions(db: Session):
        today = date.today()

        existing = db.query(Mission).count()
        if existing > 0:
            return

        missions = [
            Mission(
                title="7 dias sem delivery",
                description="Fique 7 dias sem gastar com delivery",
                type="discipline",
                difficulty="medium",
                reward_points=100,
                start_date=today,
                end_date=today + timedelta(days=7),
            ),
            Mission(
                title="Registre gastos por 7 dias",
                description="Cadastre pelo menos 1 gasto por dia durante 7 dias",
                type="habit",
                difficulty="easy",
                reward_points=50,
                start_date=today,
                end_date=today + timedelta(days=7),
            ),
        ]

        db.add_all(missions)
        db.commit()

    @staticmethod
    def list_missions(db: Session):
        return db.query(Mission).all()
