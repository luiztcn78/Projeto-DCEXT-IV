from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base  

class Atividade(Base):
    __tablename__ = "atividades"

    id_atividade = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    tipo = Column(String(50))
    dias_da_semana = Column(String(50))  
    horario = Column(String(10))  
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="atividades")
    lembretes = relationship("Lembrete", back_populates="atividade", cascade="all, delete-orphan")

