from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DiarioBase(BaseModel):
    texto: str = None
    emocao: Optional[str] = None

class DiarioCreate(DiarioBase):
    id_usuario : int
    texto: str = None
    emocao: Optional[str] = None

class DiarioUpdate(DiarioBase):
    texto: str 
    emocao: str | None = None

class DiarioResponse(DiarioBase):
    id_diario: int
    id_usuario: int
    data_registro: datetime
    emocao: Optional[str] = None

    class Config:
        orm_mode = True