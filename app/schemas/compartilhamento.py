from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class TipoDado(str, Enum):
    DIARIO = "diario"
    EMOCAO = "emocao"
    ATIVIDADE = "atividade"
    LEMBRETE = "lembrete"

class PermissaoBase(BaseModel):
    id_idoso: int
    id_familiar: int
    tipo_dado: TipoDado
    pode_ler: bool = True
    pode_ver: bool = True

class PermissaoCreate(PermissaoBase):
    pass

class PermissaoUpdate(BaseModel):
    pode_ler: Optional[bool] = None
    pode_ver: Optional[bool] = None
    data_revogacao: Optional[datetime] = None

class PermissaoResponse(PermissaoBase):
    id_permissao: int
    data_concessao: datetime
    data_revogacao: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class PermissaoRevogar(BaseModel):
    motivo: Optional[str] = None

class FamiliarDisponivel(BaseModel):
    id_usuario: int
    nome: str
    email: str
    tipo: str
    
    class Config:
        orm_mode = True

class DadoCompartilhadoRequest(BaseModel):
    tipo_dado: TipoDado
    id_idoso: int