from pydantic import BaseModel, EmailStr, constr
from typing import Literal
from datetime import datetime

class UsuarioBase(BaseModel):
    nome: constr(strip_whitespace=True, min_length=2)
    email: EmailStr
    tipo: Literal["idoso", "familiar"]

class UsuarioCreate(UsuarioBase):
    senha: constr(min_length=6)

class UsuarioUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    senha: str | None = None
    tipo: Literal["idoso", "familiar"] | None = None

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    data_criacao: datetime

    class Config:
        orm_mode = True
