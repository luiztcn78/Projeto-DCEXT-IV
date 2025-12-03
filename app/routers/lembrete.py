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
from app.crud.compartilhamento import compartilhamento_crud
from app.schemas.compartilhamento import TipoDado

router = APIRouter(prefix="/lembretes",tags=["Lembretes"])

# Endpoints existentes
@router.post("/", response_model=LembreteResponse, status_code=status.HTTP_201_CREATED)
def criar_lembrete(lembrete: LembreteCreate, db: Session = Depends(get_db)):
    return lembrete_crud.criar(db=db, data=lembrete)

@router.get("/", response_model=List[LembreteResponse])
def listar_todos(limit: int = 10, db: Session = Depends(get_db)):
    lembretes = lembrete_crud.listar_com_limit(db, limit=limit)
    return lembretes

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

@router.put("/{id_lembrete}", response_model=LembreteResponse)
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

# NOVOS ENDPOINTS PARA FAMILIARES
@router.get("/familiar/{id_familiar}/idoso/{id_idoso}", response_model=List[LembreteResponse])
def listar_lembretes_compartilhados(
    id_familiar: int,
    id_idoso: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para familiares acessarem lembretes compartilhados por um idoso
    """
    # Verificar se o familiar tem permissão
    tem_permissao = compartilhamento_crud.verificar_permissao(
        db, id_idoso, id_familiar, TipoDado.LEMBRETE
    )
    
    if not tem_permissao:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar os lembretes deste idoso"
        )
    
    return lembrete_crud.obter_por_usuario(db, id_idoso)

@router.get("/familiar/{id_familiar}/compartilhados", response_model=List[dict])
def listar_todos_lembretes_compartilhados(
    id_familiar: int,
    db: Session = Depends(get_db)
):
    """
    Lista todos os lembretes compartilhados com o familiar
    """
    # Encontrar todos os idosos que compartilham lembretes com o familiar
    permissoes = compartilhamento_crud.obter_dados_compartilhados(
        db, id_familiar, TipoDado.LEMBRETE
    )
    
    resultado = []
    for permissao in permissoes:
        lembretes = lembrete_crud.obter_por_usuario(db, permissao.id_idoso)
        
        for lembrete in lembretes:
            lembrete_info = {
                "id_lembrete": lembrete.id_lembrete,
                "id_idoso": lembrete.id_usuario,
                "nome_idoso": permissao.idoso.nome,
                "mensagem_do_lembrete": lembrete.mensagem_do_lembrete,
                "tipo_lembrete": lembrete.tipo_lembrete,
                "lido": lembrete.lido,
                "data_criacao": lembrete.data_criacao
            }
            resultado.append(lembrete_info)
    
    return resultado