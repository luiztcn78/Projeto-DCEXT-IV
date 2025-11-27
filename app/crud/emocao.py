from sqlalchemy.orm import Session
from app.models.emocao import Emocao
from app.schemas.emocao import EmocaoCreate, EmocaoUpdate


class CRUDemocoes:
    def criar(self, db: Session, data: EmocaoCreate) -> Emocao:
        emocao = Emocao(
            id_usuario=data.id_usuario,
            tipo_emocao=data.tipo_emocao,
            observacao=data.observacao,
            compartilhado=data.compartilhado,
        )
        db.add(emocao)
        db.commit()
        db.refresh(emocao)
        return emocao

    def obter_por_id(self, db: Session, id_emocao: int):
        return (
            db.query(Emocao)
            .filter(Emocao.id_emocao == id_emocao)
            .first()
        )

    def listar_por_usuario(self, db: Session, id_usuario: int):
        return (
            db.query(Emocao)
            .filter(Emocao.id_usuario == id_usuario)
            .order_by(Emocao.data_registro.desc())
            .all()
        )
    
    def listar_com_limit(self, db: Session, limit: int = 10):
        return db.query(Emocao).limit(limit).all()
    


    def atualizar(self, db: Session, id_emocao: int, data: EmocaoUpdate):
        emocao = (
            db.query(Emocao)
            .filter(Emocao.id_emocao == id_emocao)
            .first()
        )

        if not emocao:
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(emocao, key, value)

        db.commit()
        db.refresh(emocao)
        return emocao

    def deletar(self, db: Session, id_emocao: int):
        emocao = (
            db.query(Emocao)
            .filter(Emocao.id_emocao == id_emocao)
            .first()
        )

        if not emocao:
            return None

        db.delete(emocao)
        db.commit()
        return emocao


emocao_crud = CRUDemocoes()
