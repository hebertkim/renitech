# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

# ============================
# 🔥 IMPORTANTE: garante que TODOS os models sejam registrados
# ============================
import app.models  # Garante que todos os models sejam carregados

from app.database import Base, engine, wait_for_db, SessionLocal

# ============================
# IMPORTAR ROTAS
# ============================
from app.routes import (
    dashboard,
    users,
    products,
    categories,
    stock,  # Novo módulo de estoque
)

# ============================
# APP
# ============================
app = FastAPI(
    title="Renitech API",
    version="1.0.0",
    description="API para o sistema e-commerce Renitech"
)

# ============================
# ✅ SERVIR ARQUIVOS ESTÁTICOS
# ============================

# Diretório base do backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pastas existentes (avatars)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PROFILE_DIR = os.path.join(ASSETS_DIR, "img", "profile")
os.makedirs(PROFILE_DIR, exist_ok=True)
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

# Pasta para uploads de produtos
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOADS_DIR = os.path.join(STATIC_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Monta diretório estático
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# Agora as imagens podem ser acessadas via:
# http://localhost:8000/static/uploads/<nome_arquivo>.webp

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
app.include_router(products.router)  # Produtos + imagens
app.include_router(categories.router)  # Categorias
app.include_router(stock.router)  # Movimentações de estoque

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
        "message": "Renitech API rodando",
        "docs": "/docs"
    }
