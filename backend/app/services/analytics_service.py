from typing import List
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income
from app.services.analysis_service import AnalysisService
from app.schemas.dashboard import AnomalyItem


class AnomalyService:

    @staticmethod
    def detect_expense_anomalies(db: Session, std_threshold: float = 2.0) -> List[AnomalyItem]:
        anomalies: List[AnomalyItem] = []

        # Agrupa despesas por categoria
        categories = db.query(Expense.category_id).distinct().all()

        for (category_id,) in categories:
            records = (
                db.query(Expense)
                .filter(Expense.category_id == category_id)
                .order_by(Expense.date.asc())
                .all()
            )

            if len(records) < 5:
                continue  # histórico insuficiente

            values = [float(r.amount) for r in records]

            stats = AnalysisService.calculate_basic_stats(values)

            mean_val = stats["mean"]
            std_dev = stats["std_dev"]

            if std_dev == 0:
                continue

            # Analisa apenas os últimos lançamentos (ex: últimos 3)
            for r in records[-3:]:
                is_outlier = AnalysisService.detect_outlier(
                    value=float(r.amount),
                    mean_val=mean_val,
                    std_dev=std_dev,
                    threshold=std_threshold,
                )

                if is_outlier:
                    anomalies.append(
                        AnomalyItem(
                            id=r.id,
                            type="expense",
                            description=r.description,
                            amount=float(r.amount),
                            date=str(r.date),
                            category_name=r.category.name if r.category else None,
                            account_name=r.account.name if r.account else None,
                        )
                    )

        return anomalies

    @staticmethod
    def detect_income_anomalies(db: Session, std_threshold: float = 2.0) -> List[AnomalyItem]:
        anomalies: List[AnomalyItem] = []

        categories = db.query(Income.category_id).distinct().all()

        for (category_id,) in categories:
            records = (
                db.query(Income)
                .filter(Income.category_id == category_id)
                .order_by(Income.date.asc())
                .all()
            )

            if len(records) < 5:
                continue

            values = [float(r.amount) for r in records]

            stats = AnalysisService.calculate_basic_stats(values)

            mean_val = stats["mean"]
            std_dev = stats["std_dev"]

            if std_dev == 0:
                continue

            for r in records[-3:]:
                is_outlier = AnalysisService.detect_outlier(
                    value=float(r.amount),
                    mean_val=mean_val,
                    std_dev=std_dev,
                    threshold=std_threshold,
                )

                if is_outlier:
                    anomalies.append(
                        AnomalyItem(
                            id=r.id,
                            type="income",
                            description=r.description,
                            amount=float(r.amount),
                            date=str(r.date),
                            category_name=r.category.name if r.category else None,
                            account_name=r.account.name if r.account else None,
                        )
                    )

        return anomalies
