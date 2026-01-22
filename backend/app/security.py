from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.models.user import User
from app.database import SessionLocal
from typing import Optional
from passlib.context import CryptContext

# Variáveis de configuração para o JWT
SECRET_KEY = "YOUR_SECRET_KEY"  # Substitua por uma chave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # O token expira em 30 minutos

# Inicializando o gerenciador de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criar o token JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para verificar o token e obter o usuário
def verify_token(token: str) -> Optional[User]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return get_user_by_id(user_id)  # Função para buscar o usuário no banco
    except JWTError:
        return None

# Função para buscar um usuário pelo ID no banco
def get_user_by_id(user_id: str) -> Optional[User]:
    db = SessionLocal()  # Obtenha a sessão do banco
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()

# Função para verificar a senha hashada
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para buscar um usuário pelo e-mail
def get_user_by_email(db, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

# Função para autenticar o usuário (verificando e-mail e senha)
def authenticate_user(db, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if user and verify_password(password, user.password):
        return user
    return None
