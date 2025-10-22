from pydantic import BaseModel, Field, constr
from typing import Optional
from enum import Enum as PyEnum
from datetime import datetime

class TipoEmocao(str, PyEnum):
    MUITO_FELIZ = "muito_feliz"
    FELIZ = "feliz"
    NORMAL = "normal"
    TRISTE = "triste"
    MUITO_TRISTE = "muito_triste"

# Base shared fields
class EmocaoBase(BaseModel):
    id_usuario: int = Field(..., gt=0, description="ID do usuário (idoso) que registra a emoção")
    tipo_emocao: TipoEmocao
    observacao: Optional[constr(strip_whitespace=True, max_length=512)] = None
    compartilhado: Optional[bool] = False

class EmocaoCreate(EmocaoBase):
    """
    Usado ao criar um novo registro de emoção.
    id_emocao e data_registro são gerados pelo banco.
    """
    pass

class EmocaoUpdate(BaseModel):
    """
    Campos opcionais para atualização parcial/total.
    """
    tipo_emocao: Optional[TipoEmocao] = None
    observacao: Optional[constr(strip_whitespace=True, max_length=512)] = None
    compartilhado: Optional[bool] = None

class EmocaoOut(EmocaoBase):
    id_emocao: int
    data_registro: datetime

    class Config:
        orm_mode = True
