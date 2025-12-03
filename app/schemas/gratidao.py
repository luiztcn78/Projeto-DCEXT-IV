from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GratidaoBase(BaseModel):
    texto: str

class GratidaoCreate(GratidaoBase):
    id_usuario: int

class GratidaoUpdate(BaseModel):
    texto: Optional[str] = None

class GratidaoResponse(GratidaoBase):
    id_grateful: int
    id_usuario: int
    data_registro: datetime

    class Config:
        orm_mode = True
