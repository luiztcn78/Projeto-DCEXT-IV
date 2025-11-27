from pydantic import BaseModel, EmailStr, constr
from typing import Literal
from datetime import datetime
from typing import Optional, Literal

class UsuarioBase(BaseModel):
    nome: constr(strip_whitespace=True, min_length=2)
    email: EmailStr
    tipo: Literal["idoso", "familiar"]

class UsuarioCreate(UsuarioBase):
    senha: constr(min_length=6, max_length=72)


class UsuarioUpdate(BaseModel):
     nome: Optional[str] = None
     email: Optional[EmailStr] = None
     senha: Optional[str] = None
     tipo: Optional[Literal["idoso", "familiar"]] = None

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    data_criacao: datetime

    class Config:
         orm_mode = True

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: constr(strip_whitespace=True, min_length=6)
