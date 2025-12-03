import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Diario(Base):
    __tablename__ = "diarios"

    id_diario = Column(Integer, primary_key = True, index = True, autoincrement = True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable = False)
    texto = Column(String(255), nullable = False)
    emocao = Column(String(50), nullable=True)
    data_registro = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates = "diarios")