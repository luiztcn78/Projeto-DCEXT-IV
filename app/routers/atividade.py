from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.atividade import AtividadeCreate, AtividadeUpdate, AtividadeOut
from app.crud.atividade import atividade_crud
from app.crud.compartilhamento import compartilhamento_crud
from app.schemas.compartilhamento import TipoDado

router = APIRouter(prefix="/atividades", tags=["Atividades"])

# Endpoints existentes
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

# NOVOS ENDPOINTS PARA FAMILIARES
@router.get("/familiar/{id_familiar}/idoso/{id_idoso}", response_model=list[AtividadeOut])
def listar_atividades_compartilhadas(
    id_familiar: int,
    id_idoso: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para familiares acessarem atividades compartilhadas por um idoso
    """
    # Verificar se o familiar tem permissão
    tem_permissao = compartilhamento_crud.verificar_permissao(
        db, id_idoso, id_familiar, TipoDado.ATIVIDADE
    )
    
    if not tem_permissao:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar as atividades deste idoso"
        )
    
    return atividade_crud.obter_por_usuario(db, id_idoso)

@router.get("/familiar/{id_familiar}/compartilhadas", response_model=list[dict])
def listar_todas_atividades_compartilhadas(
    id_familiar: int,
    db: Session = Depends(get_db)
):
    """
    Lista todas as atividades compartilhadas com o familiar
    """
    # Encontrar todos os idosos que compartilham atividades com o familiar
    permissoes = compartilhamento_crud.obter_dados_compartilhados(
        db, id_familiar, TipoDado.ATIVIDADE
    )
    
    resultado = []
    for permissao in permissoes:
        atividades = atividade_crud.obter_por_usuario(db, permissao.id_idoso)
        
        for atividade in atividades:
            atividade_info = {
                "id_atividade": atividade.id_atividade,
                "id_idoso": atividade.id_usuario,
                "nome_idoso": permissao.idoso.nome,
                "nome": atividade.nome,
                "descricao": atividade.descricao,
                "tipo": atividade.tipo,
                "dias_da_semana": atividade.dias_da_semana,
                "horario": atividade.horario,
                "ativo": atividade.ativo,
                "data_criacao": atividade.data_criacao
            }
            resultado.append(atividade_info)
    
    return resultado