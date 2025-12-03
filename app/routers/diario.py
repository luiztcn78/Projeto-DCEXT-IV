from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.diario import DiarioCreate, DiarioUpdate, DiarioResponse
from app.crud.diario import diario_crud
from app.crud.compartilhamento import compartilhamento_crud
from app.schemas.compartilhamento import TipoDado

router = APIRouter(prefix="/diarios", tags=["diarios"])

# Endpoints existentes para idosos
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

# NOVOS ENDPOINTS PARA FAMILIARES
@router.get("/familiar/{id_familiar}/idoso/{id_idoso}", response_model=list[DiarioResponse])
def listar_diarios_compartilhados(
    id_familiar: int,
    id_idoso: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para familiares acessarem diários compartilhados por um idoso
    """
    # Verificar se o familiar tem permissão
    tem_permissao = compartilhamento_crud.verificar_permissao(
        db, id_idoso, id_familiar, TipoDado.DIARIO
    )
    
    if not tem_permissao:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar os diários deste idoso"
        )
    
    # Retornar os diários do idoso
    return diario_crud.listar_por_usuario(db, id_usuario=id_idoso)

@router.get("/familiar/{id_familiar}/compartilhados", response_model=list[dict])
def listar_todos_diarios_compartilhados(
    id_familiar: int,
    db: Session = Depends(get_db)
):
    """
    Lista todos os diários compartilhados com o familiar
    """
    # Encontrar todos os idosos que compartilham diários com o familiar
    permissoes = compartilhamento_crud.obter_dados_compartilhados(
        db, id_familiar, TipoDado.DIARIO
    )
    
    resultado = []
    for permissao in permissoes:
        diarios = diario_crud.listar_por_usuario(db, permissao.id_idoso)
        
        for diario in diarios:
            diario_info = {
                "id_diario": diario.id_diario,
                "id_idoso": diario.id_usuario,
                "nome_idoso": permissao.nome_idoso if hasattr(permissao, 'nome_idoso') else "Desconhecido",
                "texto": diario.texto,
                "emocao": diario.emocao,
                "data_registro": diario.data_registro
            }
            resultado.append(diario_info)
    
    return resultado