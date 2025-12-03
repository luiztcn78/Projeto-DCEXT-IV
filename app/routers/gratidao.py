from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.gratidao import GratidaoCreate, GratidaoUpdate, GratidaoResponse
from app.crud.gratidao import gratidao_crud

router = APIRouter(prefix="/gratidoes", tags=["Gratidoes"])

@router.post("/", response_model=GratidaoResponse, status_code=status.HTTP_201_CREATED)
def criar_gratidao(data: GratidaoCreate, db: Session = Depends(get_db)):
    return gratidao_crud.criar(db, data)

@router.get("/{id_grateful}", response_model=GratidaoResponse)
def obter_gratidao(id_grateful: int, db: Session = Depends(get_db)):
    gratidao = gratidao_crud.obter_por_id(db, id_grateful)
    if not gratidao:
        raise HTTPException(status_code=404, detail="Gratidão não encontrada.")
    return gratidao

@router.get("/usuario/{id_usuario}", response_model=list[GratidaoResponse])
def listar_gratidoes_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return gratidao_crud.listar_por_usuario(db, id_usuario)

@router.put("/{id_grateful}", response_model=GratidaoResponse)
def atualizar_gratidao(id_grateful: int, data: GratidaoUpdate, db: Session = Depends(get_db)):
    gratidao = gratidao_crud.atualizar(db, id_grateful, data)
    if not gratidao:
        raise HTTPException(status_code=404, detail="Gratidão não encontrada.")
    return gratidao

@router.delete("/{id_grateful}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_gratidao(id_grateful: int, db: Session = Depends(get_db)):
    sucesso = gratidao_crud.deletar(db, id_grateful)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Gratidão não encontrada.")
    return {"message": "Gratidão deletada com sucesso."}
