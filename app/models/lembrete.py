from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Lembrete(Base):
    __tablename__ = "lembretes"

    id_lembrete = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    id_atividade = Column(Integer, ForeignKey("atividades.id_atividade", ondelete="CASCADE"), nullable=True)
    mensagem_do_lembrete = Column(String(255), nullable=False)
    lido = Column(Boolean, default=False)
    tipo_lembrete = Column(String(50)) 
    data_criacao = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="lembretes")
    atividade = relationship("Atividade", back_populates="lembretes")
