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
# IMPORTAR ROTAS
# ============================
from app.routes import (
    dashboard,
    users,
)


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
app.include_router(dashboard.router)
app.include_router(users.router)

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
# STARTUP
# ============================
@app.on_event("startup")
def startup_event():
    print("⏳ Aguardando banco de dados...")
    wait_for_db()

    print("✅ Banco conectado!")
    print("📦 Criando tabelas...")
    Base.metadata.create_all(bind=engine)

    
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
