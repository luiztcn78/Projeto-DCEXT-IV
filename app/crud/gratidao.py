from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.gratidao import Gratidao
from app.schemas.gratidao import GratidaoCreate, GratidaoUpdate
from datetime import datetime

class CRUDGratidao:

    def criar(self, db: Session, data: GratidaoCreate) -> Gratidao:
        gratidao = Gratidao(
            id_usuario=data.id_usuario,
            texto=data.texto.strip(),
            data_registro=datetime.utcnow()
        )
        db.add(gratidao)
        db.commit()
        db.refresh(gratidao)
        return gratidao

    def obter_por_id(self, db: Session, id_grateful: int) -> Gratidao | None:
        return db.query(Gratidao).filter(Gratidao.id_grateful == id_grateful).first()

    def listar_por_usuario(self, db: Session, id_usuario: int):
        return db.query(Gratidao).filter(Gratidao.id_usuario == id_usuario).all()

    def atualizar(self, db: Session, id_grateful: int, data: GratidaoUpdate) -> Gratidao | None:
        gratidao = self.obter_por_id(db, id_grateful)
        if not gratidao:
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(gratidao, key, value)

        db.commit()
        db.refresh(gratidao)
        return gratidao

    def deletar(self, db: Session, id_grateful: int) -> bool:
        gratidao = self.obter_por_id(db, id_grateful)
        if not gratidao:
            return False

        db.delete(gratidao)
        db.commit()
        return True

gratidao_crud = CRUDGratidao()
