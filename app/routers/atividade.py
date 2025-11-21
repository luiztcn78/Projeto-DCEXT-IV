from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.atividade import AtividadeCreate, AtividadeUpdate, AtividadeOut
from app.crud.atividade import atividade_crud

router = APIRouter(prefix="/atividades", tags=["Atividades"])


@router.post("/", response_model=AtividadeOut, status_code=status.HTTP_201_CREATED)
def criar_atividade(data: AtividadeCreate, db: Session = Depends(get_db)):
    return atividade_crud.criar(db, data)

@router.get("/", response_model=list[AtividadeOut])
def listar_todas(limit: int = 10, db: Session = Depends(get_db)):
    return atividade_crud.listar_todas(db=db, limit=limit)

@router.get("/{id_atividade}", response_model=AtividadeOut)
def obter_atividade(id_atividade: int, db: Session = Depends(get_db)):
    atividade = atividade_crud.obter_por_id(db, id_atividade)
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada.")
    return atividade


@router.get("/usuario/{id_usuario}", response_model=list[AtividadeOut])
def listar_por_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return atividade_crud.obter_por_usuario(db, id_usuario)


@router.put("/{id_atividade}", response_model=AtividadeOut)
def atualizar_atividade(id_atividade: int, data: AtividadeUpdate, db: Session = Depends(get_db)):
    atividade = atividade_crud.atualizar(db, id_atividade, data)
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada.")
    return atividade


@router.patch("/{id_atividade}/toggle", response_model=AtividadeOut)
def ativar_desativar(id_atividade: int, db: Session = Depends(get_db)):
    atividade = atividade_crud.ativar_desativar(db, id_atividade)
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada.")
    return atividade


@router.delete("/{id_atividade}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_atividade(id_atividade: int, db: Session = Depends(get_db)):
    sucesso = atividade_crud.excluir(db, id_atividade)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Atividade não encontrada.")
    return
