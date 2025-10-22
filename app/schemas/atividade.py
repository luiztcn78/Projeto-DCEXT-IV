from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AtividadeBase(BaseModel):
    id_usuario: int
    nome: str
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    dias_da_semana: Optional[str] = None
    horario: Optional[str] = None
    ativo: Optional[bool] = True


class AtividadeCreate(AtividadeBase):
    pass


class AtividadeUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    dias_da_semana: Optional[str] = None
    horario: Optional[str] = None
    ativo: Optional[bool] = None


class AtividadeOut(AtividadeBase):
    id_atividade: int
    data_criacao: datetime

    class Config:
        orm_mode = True
