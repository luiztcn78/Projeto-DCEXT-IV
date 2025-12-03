from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Gratidao(Base):
    __tablename__ = "gratidoes"

    id_grateful = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    texto = Column(String(512), nullable=False)
    data_registro = Column(DateTime(timezone=True), default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="gratidoes")

