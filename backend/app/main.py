from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

# ============================
# 🔥 IMPORTANTE: garante que TODOS os models sejam registrados
# ============================
import app.models  

from app.database import Base, engine, wait_for_db, SessionLocal

# ============================
# IMPORTAR MODELS ESPECÍFICOS
# ============================
from app.models.account import Account
from app.models.alert_history import AlertHistory

# ============================
# IMPORTAR ROTAS
# ============================
from app.routes import (
    categories,
    expenses,
    incomes,
    accounts,
    dashboard,
    analysis,
    missions,
    users,
)
from app.routes import alert_router

# ============================
# IMPORTAR SERVICES
# ============================
from app.services.mission_service import MissionService
from app.services.notifications.alert_dispatcher import AlertDispatcher
from app.services.alert_service import detect_expense_anomalies

# ============================
# APP
# ============================
app = FastAPI(
    title="Finance API",
    version="1.0.0",
    description="API de controle financeiro pessoal"
)

# ============================
# ✅ SERVIR ARQUIVOS ESTÁTICOS (AVATARS)
# ============================

# Diretório base do backend: app/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# app/assets
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# app/assets/img/profile
PROFILE_DIR = os.path.join(ASSETS_DIR, "img", "profile")

# Garante que a pasta exista
os.makedirs(PROFILE_DIR, exist_ok=True)

# Permite acessar:
# http://localhost:8000/assets/img/profile/arquivo.png
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

# ============================
# ✅ CORS (FRONTEND VUE)
# ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois podemos restringir para http://localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# REGISTRAR ROTAS
# ============================
app.include_router(expenses.router)
app.include_router(incomes.router)
app.include_router(categories.router)
app.include_router(accounts.router)
app.include_router(dashboard.router)
app.include_router(analysis.router)
app.include_router(missions.router)
app.include_router(alert_router.router)  # ⚡ ALERTAS
app.include_router(users.router)         # ⚡ USERS

# ============================
# DEPENDÊNCIA DB
# ============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================
# FUNÇÃO: GARANTIR CONTA PADRÃO
# ============================
def ensure_default_account():
    db: Session = SessionLocal()
    try:
        acc = db.query(Account).filter(Account.name == "Conta Padrão").first()
        if not acc:
            acc = Account(name="Conta Padrão", balance=0)
            db.add(acc)
            db.commit()
            db.refresh(acc)
            print("💰 Conta Padrão criada automaticamente.")
        else:
            print("💰 Conta Padrão já existe.")
        return acc
    finally:
        db.close()

# ============================
# FUNÇÃO: REGISTRAR ALERTA NO BANCO
# ============================
def save_alert_history(db: Session, title: str, level: str, message: str):
    alert = AlertHistory(title=title, level=level, message=message)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    print(f"📝 Alerta registrado no histórico: {title}")

# ============================
# STARTUP
# ============================
@app.on_event("startup")
def startup_event():
    print("⏳ Aguardando banco de dados...")
    wait_for_db()

    print("✅ Banco conectado!")
    print("📦 Criando tabelas...")
    Base.metadata.create_all(bind=engine)

    print("🏦 Verificando conta padrão...")
    ensure_default_account()

    # ============================
    # Gerar missões iniciais
    # ============================
    print("🎯 Verificando missões financeiras...")
    db = SessionLocal()
    try:
        MissionService.generate_default_missions(db)
        print("🏆 Missões prontas!")
    finally:
        db.close()

    # ============================
    # Enviar alertas automáticos
    # ============================
    print("📣 Enviando alertas automáticos (somente e-mail por enquanto)...")
    db = SessionLocal()
    try:
        users_list = [
            {"email": "m.hebertsouza@gmail.com"}  # WhatsApp temporariamente removido
        ]
        AlertDispatcher.send_alerts(db, users_list, auto_whatsapp=False)

        # 🔹 ALERTA DE TESTE
        print("🧪 Criando alerta de teste no histórico...")
        save_alert_history(
            db,
            title="Alerta de Teste",
            level="info",
            message="Este é um alerta de teste enviado na startup."
        )
        print("✅ Alerta de teste registrado com sucesso!")
    finally:
        db.close()

    # ============================
    # Detectar despesas fora do padrão
    # ============================
    print("⚠️ Verificando despesas fora do padrão...")
    db = SessionLocal()
    try:
        anomalies = detect_expense_anomalies(db, user_id=1)  # testar com user_id=1
        for alert in anomalies:
            save_alert_history(
                db,
                title=alert.mensagem,
                level="warning",
                message=f"Valor: {alert.valor} | Categoria ID: {alert.category_id}"
            )
        print(f"✅ {len(anomalies)} alertas de despesas fora do padrão gerados.")
    finally:
        db.close()

    print("🚀 API pronta para uso!")

# ============================
# HEALTH CHECK
# ============================
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Finance API rodando",
        "docs": "/docs"
    }
