from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

from app.models.expense import Expense
from app.models.income import Income


def calculate_financial_health(db: Session):
    today = date.today()
    six_months_ago = today - timedelta(days=180)

    # =========================
    # BUSCAR DADOS
    # =========================

    expenses = db.query(Expense).filter(Expense.date >= six_months_ago).all()
    incomes = db.query(Income).filter(Income.date >= six_months_ago).all()

    total_expenses = sum(e.amount for e in expenses)
    total_incomes = sum(i.amount for i in incomes)

    # =========================
    # SCORE BASE
    # =========================

    score = 50  # começa neutro
    positives = []
    alerts = []
    recommendations = []

    # =========================
    # REGRA 1: Lucro ou prejuízo
    # =========================

    if total_incomes > total_expenses:
        score += 20
        positives.append("Você está operando com lucro nos últimos meses.")
    else:
        score -= 30
        alerts.append("Você está gastando mais do que ganha.")
        recommendations.append("Reduzir despesas ou aumentar receitas imediatamente.")

    # =========================
    # REGRA 2: Proporção gastos / receita
    # =========================

    if total_incomes > 0:
        ratio = total_expenses / total_incomes
        if ratio < 0.7:
            score += 10
            positives.append("Seu nível de gastos está bem controlado.")
        elif ratio < 0.9:
            alerts.append("Seus gastos estão altos em relação à receita.")
            recommendations.append("Tentar reduzir despesas fixas.")
        else:
            score -= 20
            alerts.append("Seus gastos estão perigosamente próximos ou acima da receita.")
            recommendations.append("Cortar custos com urgência.")

    # =========================
    # REGRA 3: Frequência de despesas
    # =========================

    if len(expenses) > 100:
        alerts.append("Você possui muitas despesas recorrentes.")
        recommendations.append("Avaliar e eliminar despesas desnecessárias.")

    # =========================
    # REGRA 4: Dependência de poucas receitas
    # =========================

    categories_income = db.query(
        Income.category_id, func.count(Income.id)
    ).group_by(Income.category_id).all()

    if len(categories_income) <= 1 and len(incomes) > 0:
        score -= 10
        alerts.append("Você depende de uma única fonte de renda.")
        recommendations.append("Diversificar fontes de receita.")

    # =========================
    # LIMITES DO SCORE
    # =========================

    if score < 0:
        score = 0
    if score > 100:
        score = 100

    # =========================
    # CLASSIFICAÇÃO
    # =========================

    if score >= 75:
        status = "Saudável"
        summary = "Sua saúde financeira está ótima."
    elif score >= 45:
        status = "Atenção"
        summary = "Sua saúde financeira exige atenção."
    else:
        status = "Crítico"
        summary = "Sua situação financeira é preocupante."

    # =========================
    # FALLBACKS
    # =========================

    if not positives:
        positives.append("Nenhum indicador positivo relevante no período.")

    if not alerts:
        alerts.append("Nenhum alerta crítico identificado.")

    # =========================
    # RESULTADO FINAL
    # =========================

    return {
        "score": score,
        "status": status,
        "summary": summary,
        "positives": positives,
        "alerts": alerts,
        "recommendations": recommendations
    }
