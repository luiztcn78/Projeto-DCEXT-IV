from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate, UsuarioLogin
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

# Listar usuários com limite
@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(limit: int = 10, db: Session = Depends(get_db)):
    return usuario_crud.listar_com_limit(db, limit)

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = usuario_crud.atualizar(db, id_usuario=usuario_id, data=usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

# Excluir usuário
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_usuario(usuario_id: int, db: Session = Depends(get_db)):
    sucesso = usuario_crud.excluir(db, id_usuario=usuario_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return



@router.post("/login", response_model=UsuarioResponse)
def login(data: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = usuario_crud.obter_por_email(db, email=data.email)
    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    if usuario.senha != data.senha:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    return usuario
