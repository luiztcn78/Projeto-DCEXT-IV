from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.compartilhamento import compartilhamento_crud
from app.schemas.compartilhamento import TipoDado

def verificar_permissao_familiar(
    id_idoso: int,
    id_familiar: int,
    tipo_dado: TipoDado,
    db: Session = Depends(get_db)
):
    """
    Dependência para verificar se um familiar tem permissão para acessar dados de um idoso
    """
    tem_permissao = compartilhamento_crud.verificar_permissao(db, id_idoso, id_familiar, tipo_dado)
    
    if not tem_permissao:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar estes dados"
        )
    
    return True