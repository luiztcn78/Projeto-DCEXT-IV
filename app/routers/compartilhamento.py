from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.compartilhamento import (
    PermissaoCreate, 
    PermissaoResponse, 
    PermissaoUpdate,
    PermissaoRevogar,
    FamiliarDisponivel,
    DadoCompartilhadoRequest,
    TipoDado
)
from app.crud.compartilhamento import compartilhamento_crud

router = APIRouter(prefix="/compartilhamento", tags=["Compartilhamento"])

@router.post("/", response_model=PermissaoResponse, status_code=status.HTTP_201_CREATED)
def conceder_permissao(permissao: PermissaoCreate, db: Session = Depends(get_db)):
    """
    Concede permissão a um familiar para acessar dados de um idoso
    """
    return compartilhamento_crud.criar_permissao(db, permissao)

@router.get("/idoso/{id_idoso}", response_model=List[PermissaoResponse])
def listar_permissoes_idoso(id_idoso: int, ativas: bool = True, db: Session = Depends(get_db)):
    """
    Lista todas as permissões concedidas por um idoso
    """
    return compartilhamento_crud.listar_permissoes_por_idoso(db, id_idoso, ativas)

@router.get("/familiar/{id_familiar}", response_model=List[PermissaoResponse])
def listar_permissoes_familiar(id_familiar: int, ativas: bool = True, db: Session = Depends(get_db)):
    """
    Lista todas as permissões recebidas por um familiar
    """
    return compartilhamento_crud.listar_permissoes_por_familiar(db, id_familiar, ativas)

@router.get("/{id_permissao}", response_model=PermissaoResponse)
def obter_permissao(id_permissao: int, db: Session = Depends(get_db)):
    """
    Obtém uma permissão específica pelo ID
    """
    permissao = compartilhamento_crud.obter_permissao(db, id_permissao)
    if not permissao:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")
    return permissao

@router.put("/{id_permissao}", response_model=PermissaoResponse)
def atualizar_permissao(id_permissao: int, permissao: PermissaoUpdate, db: Session = Depends(get_db)):
    """
    Atualiza uma permissão existente
    """
    return compartilhamento_crud.atualizar_permissao(db, id_permissao, permissao)

@router.post("/{id_permissao}/revogar", response_model=PermissaoResponse)
def revogar_permissao(id_permissao: int, motivo: PermissaoRevogar = None, db: Session = Depends(get_db)):
    """
    Revoga uma permissão (marca como revogada)
    """
    motivo_texto = motivo.motivo if motivo else None
    return compartilhamento_crud.revogar_permissao(db, id_permissao, motivo_texto)

@router.get("/idoso/{id_idoso}/familiares-disponiveis")
def listar_familiares_disponiveis(id_idoso: int, db: Session = Depends(get_db)):
    """
    Lista todos os familiares disponíveis para um idoso,
    incluindo informações sobre permissões já concedidas
    """
    return compartilhamento_crud.listar_familiares_disponiveis(db, id_idoso)

@router.post("/verificar")
def verificar_permissao(
    id_idoso: int,
    id_familiar: int,
    tipo_dado: TipoDado,
    db: Session = Depends(get_db)
):
    """
    Verifica se um familiar tem permissão para acessar um tipo de dado de um idoso
    """
    tem_permissao = compartilhamento_crud.verificar_permissao(db, id_idoso, id_familiar, tipo_dado)
    return {"tem_permissao": tem_permissao}

@router.post("/familiar/{id_familiar}/dados-compartilhados")
def obter_dados_compartilhados_familiar(
    id_familiar: int,
    request: DadoCompartilhadoRequest,
    db: Session = Depends(get_db)
):
    """
    Retorna todos os idosos que compartilham um tipo específico de dado com o familiar
    """
    permissoes = compartilhamento_crud.obter_dados_compartilhados(db, id_familiar, request.tipo_dado)
    
    resultado = []
    for permissao in permissoes:
        # Buscar nome do idoso
        from app.models.usuario import Usuario
        idoso = db.query(Usuario).filter(Usuario.id_usuario == permissao.id_idoso).first()
        
        idoso_info = {
            "id_idoso": permissao.id_idoso,
            "nome_idoso": idoso.nome if idoso else "Desconhecido",
            "tipo_dado": permissao.tipo_dado.value,
            "data_concessao": permissao.data_concessao,
            "pode_ler": permissao.pode_ler,
            "pode_ver": permissao.pode_ver
        }
        resultado.append(idoso_info)
    
    return resultado