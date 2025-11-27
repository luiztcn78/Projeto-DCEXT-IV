from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.emocao import emocao_crud
from app.schemas.emocao import EmocaoCreate, EmocaoResponse, EmocaoUpdate

router = APIRouter(prefix="/emocoes", tags=["emocoes"])


@router.post("/", response_model=EmocaoResponse, status_code=status.HTTP_201_CREATED)
def criar_emocao(data: EmocaoCreate, db: Session = Depends(get_db)):
    emocao = emocao_crud.criar(db, data)
    return emocao


@router.get("/{id_emocao}", response_model=EmocaoResponse)
def obter_emocao(id_emocao: int, db: Session = Depends(get_db)):
    emocao = emocao_crud.obter_por_id(db, id_emocao)
    if not emocao:
        raise HTTPException(status_code=404, detail="Emoção não encontrada.")
    return emocao


@router.get("/usuario/{id_usuario}", response_model=list[EmocaoResponse])
def listar_por_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return emocao_crud.listar_por_usuario(db, id_usuario)


@router.get("/limit/{limit}", response_model=list[EmocaoResponse])
def listar_com_limit(limit: int = 10, db: Session = Depends(get_db)):
    emocoes = emocao_crud.listar_com_limit(db, limit=limit)
    
    if emocoes is None:
        raise HTTPException(status_code=500, detail="Erro interno ao buscar emoções.")

    return emocoes


@router.put("/{id_emocao}", response_model=EmocaoResponse)
def atualizar_emocao(id_emocao: int, data: EmocaoUpdate, db: Session = Depends(get_db)):
    emocao = emocao_crud.atualizar(db, id_emocao, data)
    if not emocao:
        raise HTTPException(status_code=404, detail="Emoção não encontrada.")
    return emocao


@router.delete("/{id_emocao}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_emocao(id_emocao: int, db: Session = Depends(get_db)):
    emocao = emocao_crud.deletar(db, id_emocao)
    if not emocao:
        raise HTTPException(status_code=404, detail="Emoção não encontrada.")
    return None
