from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.lembrete import (
    LembreteCreate,
    LembreteUpdate,
    LembreteResponse,
)
from app.crud.lembrete import lembrete_crud

router = APIRouter(prefix="/lembretes",tags=["Lembretes"])


@router.post("/", response_model=LembreteResponse, status_code=status.HTTP_201_CREATED)
def criar_lembrete(lembrete: LembreteCreate, db: Session = Depends(get_db)):
    return lembrete_crud.criar(db=db, data=lembrete)


@router.get("/{id_lembrete}", response_model=LembreteResponse)
def obter_lembrete(id_lembrete: int, db: Session = Depends(get_db)):
    lembrete = lembrete_crud.obter_por_id(db, id_lembrete)
    if not lembrete:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado")
    return lembrete


@router.get("/usuario/{id_usuario}", response_model=List[LembreteResponse])
def listar_por_usuario(id_usuario: int, db: Session = Depends(get_db)):
    lembretes = lembrete_crud.obter_por_usuario(db, id_usuario)
    return lembretes


@router.patch("/{id_lembrete}", response_model=LembreteResponse)
def atualizar_lembrete(id_lembrete: int, data: LembreteUpdate, db: Session = Depends(get_db)):
    lembrete = lembrete_crud.atualizar(db, id_lembrete, data)
    if not lembrete:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado")
    return lembrete


@router.patch("/{id_lembrete}/lido", response_model=LembreteResponse)
def marcar_como_lido(id_lembrete: int, db: Session = Depends(get_db)):
    lembrete = lembrete_crud.marcar_como_lido(db, id_lembrete)
    if not lembrete:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado")
    return lembrete


@router.delete("/{id_lembrete}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_lembrete(id_lembrete: int, db: Session = Depends(get_db)):
    sucesso = lembrete_crud.excluir(db, id_lembrete)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado")
    return None
