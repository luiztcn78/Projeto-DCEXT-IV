from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LembreteBase(BaseModel):
    id_usuario: int
    id_atividade: Optional[int] = None
    mensagem_do_lembrete: str
    lido: Optional[bool] = False
    tipo_lembrete: Optional[str] = None


class LembreteCreate(LembreteBase):
    pass


class LembreteUpdate(BaseModel):
    mensagem_do_lembrete: Optional[str] = None
    lido: Optional[bool] = None
    tipo_lembrete: Optional[str] = None


class LembreteOut(LembreteBase):
    id_lembrete: int
    data_criacao: datetime

    class Config:
        orm_mode = True
