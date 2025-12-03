from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False) 
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    # Relações
    atividades = relationship("Atividade", back_populates="usuario", cascade="all, delete-orphan")
    lembretes = relationship("Lembrete", back_populates="usuario", cascade="all, delete-orphan")
    diarios = relationship("Diario", back_populates="usuario", cascade="all, delete-orphan")
    emocoes = relationship("Emocao", back_populates="usuario", cascade="all, delete-orphan")
    gratidoes = relationship("Gratidao", back_populates="usuario", cascade="all, delete-orphan")