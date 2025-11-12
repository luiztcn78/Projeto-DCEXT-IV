from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.crud.usuario import usuario_crud

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se email já existe
    db_usuario = usuario_crud.obter_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    return usuario_crud.criar(db=db, data=usuario)

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = usuario_crud.obter_por_id(db, id_usuario=usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

@router.get("/email/{email}", response_model=UsuarioResponse)
def obter_usuario_por_email(email: str, db: Session = Depends(get_db)):
    db_usuario = usuario_crud.obter_por_email(db, email=email)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario