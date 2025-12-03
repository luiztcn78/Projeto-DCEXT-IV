from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.diario import DiarioCreate, DiarioUpdate, DiarioResponse
from app.crud.diario import diario_crud

router = APIRouter(prefix="/diarios", tags=["diarios"])

@router.post("/", response_model=DiarioResponse)
def criar_diario(diario: DiarioCreate, db: Session = Depends(get_db)):
    return diario_crud.criar(db, diario)

@router.get("/{diario_id}", response_model=DiarioResponse)
def obter_diario(diario_id: int, db: Session = Depends(get_db)):
    db_diario = diario_crud.obter_por_id(db, id_diario=diario_id)
    if not db_diario:
        raise HTTPException(status_code=404, detail="Diário não encontrado")
    return db_diario

@router.get("/usuario/{id_usuario}", response_model=list[DiarioResponse])
def listar_diarios_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return diario_crud.listar_por_usuario(db, id_usuario=id_usuario)

@router.put("/{diario_id}", response_model=DiarioResponse)
def atualizar_diario(diario_id: int, diario: DiarioUpdate, db: Session = Depends(get_db)):
    db_diario = diario_crud.atualizar(db, id_diario=diario_id, data=diario)
    if not db_diario:
        raise HTTPException(status_code=404, detail="Diário não encontrado")
    return db_diario

@router.delete("/{diario_id}")
def deletar_diario(diario_id: int, db: Session = Depends(get_db)):
    db_diario = diario_crud.deletar(db, id_diario=diario_id)
    if not db_diario:
        raise HTTPException(status_code=404, detail="Diário não encontrado")
    return {"message": "Diário deletado com sucesso"}