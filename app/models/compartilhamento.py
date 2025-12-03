from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class TipoDado(str, enum.Enum):
    DIARIO = "diario"
    EMOCAO = "emocao"
    ATIVIDADE = "atividade"
    LEMBRETE = "lembrete"

class PermissaoCompartilhamento(Base):
    __tablename__ = "permissoes_compartilhamento"
    
    id_permissao = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_idoso = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    id_familiar = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    tipo_dado = Column(Enum(TipoDado), nullable=False)
    pode_ler = Column(Boolean, default=True, nullable=False)
    pode_ver = Column(Boolean, default=True, nullable=False)
    data_concessao = Column(DateTime(timezone=True), server_default=func.now())
    data_revogacao = Column(DateTime(timezone=True), nullable=True)
    
    # Relações
    idoso = relationship("Usuario", foreign_keys=[id_idoso], backref="permissoes_concedidas")
    familiar = relationship("Usuario", foreign_keys=[id_familiar], backref="permissoes_recebidas")