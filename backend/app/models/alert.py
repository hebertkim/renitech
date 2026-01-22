from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # se users.id é Integer, tudo certo
    category_id = Column(String(36), ForeignKey("categories.id"))  # ✅ Tipo compatível com Category.id
    tipo = Column(String(50))       # tamanho definido ✅
    mensagem = Column(String(255))  # tamanho definido ✅
    valor = Column(Numeric(10, 2))  # ✅ Numeric para valores monetários
    threshold = Column(Numeric(10, 2))  # ✅ Numeric para limites
    data = Column(Date)
