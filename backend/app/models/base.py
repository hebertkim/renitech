# app/models/base.py
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, DateTime, func, String
import uuid

@as_declarative()
class Base:
    id: str
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        # Nome da tabela no plural
        return cls.__name__.lower() + "s"

    # PK padrão UUID
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    # Timestamps padronizados
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
