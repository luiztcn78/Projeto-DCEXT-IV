from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DiarioBase(BaseModel):
    texto: str = None

class DiarioCreate(DiarioBase):
    id_usuario : int
    texto: str = None

class DiarioUpdate(DiarioBase):
    texto: str 

class DiarioResponse(DiarioBase):
    id_diario: int
    id_usuario: int
    data_registro = datetime

    class Config:
        orm_mode = True