import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

# ============================
# Configurações de ambiente
# ============================

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "finance_user")
DB_PASS = os.getenv("DB_PASS", "user123")
DB_NAME = os.getenv("DB_NAME", "finance_db")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ============================
# SQLAlchemy
# ============================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ============================
# Dependency para FastAPI
# ============================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================
# Esperar o banco subir
# ============================

def wait_for_db(max_retries: int = 60, delay: int = 2):
    print("⏳ Aguardando banco de dados...")

    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Banco de dados disponível!")
            return
        except OperationalError:
            print(f"⏳ Tentativa {attempt+1}/{max_retries} - banco ainda não disponível...")
            time.sleep(delay)

    raise Exception("❌ Banco de dados não ficou disponível a tempo")
