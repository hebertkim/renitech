# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# ============================
# IMPORTANTE: garante que todos os models sejam registrados
# ============================
from app import models  # noqa: F401

from app.database import Base, engine, wait_for_db, SessionLocal

# ============================
# IMPORTAR ROTAS
# ============================
from app.routes import (
    dashboard as dashboard_routes,   # 🔒 admin
    users as users_routes,           # 🔒 admin / auth
    products as products_routes,     # 🌐 público + admin
    categories as categories_routes, # 🌐 público + admin
    stock as stock_routes,           # 🔒 admin
    orders as orders_routes,         # 🔒 admin
)

# ============================
# APP
# ============================
app = FastAPI(
    title="Renitech API",
    version="1.0.0",
    description="API para o sistema e-commerce Renitech",
)

# ============================
# SERVIR ARQUIVOS ESTÁTICOS
# ============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PROFILE_DIR = os.path.join(ASSETS_DIR, "img", "profile")
os.makedirs(PROFILE_DIR, exist_ok=True)

STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOADS_DIR = os.path.join(STATIC_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ============================
# CORS (FRONTEND VUE)
# ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Em produção, restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# REGISTRAR ROTAS
# ============================
app.include_router(users_routes.router)       # auth, perfil, etc
app.include_router(products_routes.router)    # público + admin
app.include_router(categories_routes.router)  # público + admin

# 🔒 Rotas administrativas
app.include_router(dashboard_routes.router)
app.include_router(stock_routes.router)
app.include_router(orders_routes.router)

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
    print("Aguardando banco de dados...")
    wait_for_db()
    print("Banco conectado!")

    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)

    print("API pronta para uso!")

# ============================
# HEALTH CHECK
# ============================
@app.get("/", tags=["Root"])
def root():
    return {"status": "ok", "message": "Renitech API rodando", "docs": "/docs"}
