from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.emocao import emocao_crud
from app.schemas.emocao import EmocaoCreate, EmocaoResponse, EmocaoUpdate
from app.crud.compartilhamento import compartilhamento_crud
from app.schemas.compartilhamento import TipoDado

router = APIRouter(prefix="/emocoes", tags=["emocoes"])

# Endpoints existentes para idosos
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

# NOVOS ENDPOINTS PARA FAMILIARES
@router.get("/familiar/{id_familiar}/idoso/{id_idoso}", response_model=list[EmocaoResponse])
def listar_emocoes_compartilhadas(
    id_familiar: int,
    id_idoso: int,
    compartilhadas: bool = True,
    db: Session = Depends(get_db)
):
    """
    Endpoint para familiares acessarem emoções compartilhadas por um idoso
    """
    # Verificar se o familiar tem permissão
    tem_permissao = compartilhamento_crud.verificar_permissao(
        db, id_idoso, id_familiar, TipoDado.EMOCAO
    )
    
    if not tem_permissao:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar as emoções deste idoso"
        )
    
    # Obter todas as emoções do idoso
    emocoes = emocao_crud.listar_por_usuario(db, id_idoso)
    
    # Filtrar apenas as compartilhadas, se solicitado
    if compartilhadas:
        emocoes = [e for e in emocoes if e.compartilhado]
    
    return emocoes

@router.get("/familiar/{id_familiar}/compartilhadas", response_model=list[dict])
def listar_todas_emocoes_compartilhadas(
    id_familiar: int,
    compartilhadas: bool = True,
    db: Session = Depends(get_db)
):
    """
    Lista todas as emoções compartilhadas com o familiar
    """
    # Encontrar todos os idosos que compartilham emoções com o familiar
    permissoes = compartilhamento_crud.obter_dados_compartilhados(
        db, id_familiar, TipoDado.EMOCAO
    )
    
    resultado = []
    for permissao in permissoes:
        emocoes = emocao_crud.listar_por_usuario(db, permissao.id_idoso)
        
        for emocao in emocoes:
            # Apenas adicionar se for compartilhada (quando compartilhadas=True)
            if not compartilhadas or emocao.compartilhado:
                emocao_info = {
                    "id_emocao": emocao.id_emocao,
                    "id_idoso": emocao.id_usuario,
                    "nome_idoso": permissao.idoso.nome,
                    "tipo_emocao": emocao.tipo_emocao.value,
                    "observacao": emocao.observacao,
                    "compartilhado": emocao.compartilhado,
                    "data_registro": emocao.data_registro
                }
                resultado.append(emocao_info)
    
    return resultado