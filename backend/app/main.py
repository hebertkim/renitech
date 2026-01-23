# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# ============================
# 🔥 IMPORTANTE: garante que TODOS os models sejam registrados
# ============================
import app.models  # Todos os models carregados

from app.database import Base, engine, wait_for_db, SessionLocal

# ============================
# IMPORTAR ROTAS
# ============================
from app.routes import (
    dashboard,
    users,
    products,
    categories,
    stock,   # Movimentações de estoque
    orders,    # Pedidos
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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Diretórios para avatars e uploads
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PROFILE_DIR = os.path.join(ASSETS_DIR, "img", "profile")
os.makedirs(PROFILE_DIR, exist_ok=True)

STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOADS_DIR = os.path.join(STATIC_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Montagem
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ============================
# ✅ CORS (FRONTEND VUE)
# ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para desenvolvimento; em produção, restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# REGISTRAR ROTAS
# ============================
# Swagger vai separar pelas tags definidas nos routers
app.include_router(dashboard.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(stock.router)
app.include_router(orders.router)  # Pedidos

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
@app.get("/", tags=["Root"])
def root():
    return {
        "status": "ok",
        "message": "Renitech API rodando",
        "docs": "/docs"
    }
