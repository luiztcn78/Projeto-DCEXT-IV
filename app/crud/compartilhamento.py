from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from app.models.compartilhamento import PermissaoCompartilhamento, TipoDado
from app.models.usuario import Usuario
from app.schemas.compartilhamento import PermissaoCreate, PermissaoUpdate
from fastapi import HTTPException, status

class CRUDCompartilhamento:
    
    def criar_permissao(self, db: Session, data: PermissaoCreate) -> PermissaoCompartilhamento:
        # Verificar se idoso existe e é do tipo idoso
        idoso = db.query(Usuario).filter(
            Usuario.id_usuario == data.id_idoso,
            Usuario.tipo == "idoso"
        ).first()
        
        if not idoso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Idoso não encontrado"
            )
        
        # Verificar se familiar existe e é do tipo familiar
        familiar = db.query(Usuario).filter(
            Usuario.id_usuario == data.id_familiar,
            Usuario.tipo == "familiar"
        ).first()
        
        if not familiar:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Familiar não encontrado"
            )
        
        # Verificar se já existe permissão ativa
        permissao_existente = db.query(PermissaoCompartilhamento).filter(
            PermissaoCompartilhamento.id_idoso == data.id_idoso,
            PermissaoCompartilhamento.id_familiar == data.id_familiar,
            PermissaoCompartilhamento.tipo_dado == data.tipo_dado,
            PermissaoCompartilhamento.data_revogacao.is_(None)
        ).first()
        
        if permissao_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permissão já concedida para este familiar"
            )
        
        permissao = PermissaoCompartilhamento(
            id_idoso=data.id_idoso,
            id_familiar=data.id_familiar,
            tipo_dado=data.tipo_dado,
            pode_ler=data.pode_ler,
            pode_ver=data.pode_ver
        )
        
        db.add(permissao)
        db.commit()
        db.refresh(permissao)
        return permissao
    
    def obter_permissao(self, db: Session, id_permissao: int) -> PermissaoCompartilhamento:
        return db.query(PermissaoCompartilhamento).filter(
            PermissaoCompartilhamento.id_permissao == id_permissao
        ).first()
    
    def listar_permissoes_por_idoso(self, db: Session, id_idoso: int, ativas: bool = True):
        query = db.query(PermissaoCompartilhamento).filter(
            PermissaoCompartilhamento.id_idoso == id_idoso
        )
        
        if ativas:
            query = query.filter(PermissaoCompartilhamento.data_revogacao.is_(None))
        
        return query.order_by(PermissaoCompartilhamento.data_concessao.desc()).all()
    
    def listar_permissoes_por_familiar(self, db: Session, id_familiar: int, ativas: bool = True):
        query = db.query(PermissaoCompartilhamento).filter(
            PermissaoCompartilhamento.id_familiar == id_familiar
        )
        
        if ativas:
            query = query.filter(PermissaoCompartilhamento.data_revogacao.is_(None))
        
        return query.order_by(PermissaoCompartilhamento.data_concessao.desc()).all()
    
    def verificar_permissao(self, db: Session, id_idoso: int, id_familiar: int, tipo_dado: TipoDado) -> bool:
        permissao = db.query(PermissaoCompartilhamento).filter(
            PermissaoCompartilhamento.id_idoso == id_idoso,
            PermissaoCompartilhamento.id_familiar == id_familiar,
            PermissaoCompartilhamento.tipo_dado == tipo_dado,
            PermissaoCompartilhamento.data_revogacao.is_(None),
            PermissaoCompartilhamento.pode_ver == True
        ).first()
        
        return permissao is not None
    
    def atualizar_permissao(self, db: Session, id_permissao: int, data: PermissaoUpdate) -> PermissaoCompartilhamento:
        permissao = self.obter_permissao(db, id_permissao)
        
        if not permissao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permissão não encontrada"
            )
        
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(permissao, key, value)
        
        db.commit()
        db.refresh(permissao)
        return permissao
    
    def revogar_permissao(self, db: Session, id_permissao: int, motivo: str = None) -> PermissaoCompartilhamento:
        permissao = self.obter_permissao(db, id_permissao)
        
        if not permissao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permissão não encontrada"
            )
        
        permissao.data_revogacao = datetime.now()
        db.commit()
        db.refresh(permissao)
        return permissao
    
    def listar_familiares_disponiveis(self, db: Session, id_idoso: int):
        # Retorna todos os familiares que NÃO são o próprio idoso
        familiares = db.query(Usuario).filter(
            Usuario.tipo == "familiar",
            Usuario.id_usuario != id_idoso
        ).all()
        
        # Adiciona informação sobre quais permissões já foram concedidas
        resultado = []
        for familiar in familiares:
            permissoes = db.query(PermissaoCompartilhamento).filter(
                PermissaoCompartilhamento.id_idoso == id_idoso,
                PermissaoCompartilhamento.id_familiar == familiar.id_usuario,
                PermissaoCompartilhamento.data_revogacao.is_(None)
            ).all()
            
            tipos_concedidos = [p.tipo_dado.value for p in permissoes]
            
            familiar_info = {
                "id_usuario": familiar.id_usuario,
                "nome": familiar.nome,
                "email": familiar.email,
                "tipo": familiar.tipo,
                "permissoes_concedidas": tipos_concedidos
            }
            resultado.append(familiar_info)
        
        return resultado
    
    def obter_dados_compartilhados(self, db: Session, id_familiar: int, tipo_dado: TipoDado):
        # Encontra todos os idosos que concederam permissão ao familiar
        permissoes = db.query(PermissaoCompartilhamento).filter(
            PermissaoCompartilhamento.id_familiar == id_familiar,
            PermissaoCompartilhamento.tipo_dado == tipo_dado,
            PermissaoCompartilhamento.data_revogacao.is_(None),
            PermissaoCompartilhamento.pode_ver == True
        ).all()
        
        return permissoes

compartilhamento_crud = CRUDCompartilhamento()