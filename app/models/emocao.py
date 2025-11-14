from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from app.database import Base

class TipoEmocao(PyEnum):
    MUITO_FELIZ = "muito_feliz"
    FELIZ = "feliz"
    NORMAL = "normal"
    TRISTE = "triste"
    MUITO_TRISTE = "muito_triste"

class Emocao(Base):
    """
    Tabela: emocoes
    Campos:
      - id_emocao: PK
      - id_usuario: FK -> usuarios.id_usuario
      - tipo_emocao: enum (valores no TipoEmocao)
      - observacao: texto opcional para comentários do usuário
      - compartilhado: bool indicando se o idoso permitiu que familiares vejam este registro
      - data_registro: timestamp do registro (default now)
    """

    __tablename__ = "emocoes"

    id_emocao = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    tipo_emocao = Column(SQLAEnum(TipoEmocao, name="tipo_emocao_enum"), nullable=False)
    observacao = Column(String(512), nullable=True)
    compartilhado = Column(Boolean, nullable=False, default=False)
    data_registro = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship com Usuario.
    # Usamos backref para não precisar editar o model Usuario existente.
    usuario = relationship("Usuario", back_populates="emocoes")