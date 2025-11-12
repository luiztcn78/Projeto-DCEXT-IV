from sqlalchemy.orm import Session
from app.models.lembrete import Lembrete
from app.schemas.lembrete import LembreteCreate, LembreteUpdate
from fastapi import HTTPException, status

class CRUDLembrete:
    def criar(self, db: Session, data: LembreteCreate) -> Lembrete:
        lembrete_existente = db.query(Lembrete).filter(
            Lembrete.id_usuario == data.id_usuario,
            Lembrete.mensagem_do_lembrete == data.mensagem_do_lembrete.strip()
        ).first()
        if lembrete_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um lembrete com essa mensagem para este usuário."
            )

        lembrete = Lembrete(
            id_usuario=data.id_usuario,
            id_atividade=data.id_atividade,
            mensagem_do_lembrete=data.mensagem_do_lembrete.strip(),
            tipo_lembrete=data.tipo_lembrete,
        )
        db.add(lembrete)
        db.commit()
        db.refresh(lembrete)
        return lembrete

    def atualizar(self, db: Session, id_lembrete: int, data: LembreteUpdate) -> Lembrete | None:
        lembrete = self.obter_por_id(db, id_lembrete)
        if not lembrete:
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(lembrete, key, value)

        db.commit()
        db.refresh(lembrete)
        return lembrete

    def marcar_como_lido(self, db: Session, id_lembrete: int) -> Lembrete | None:
        lembrete = self.obter_por_id(db, id_lembrete)
        if not lembrete:
            return None

        lembrete.lido = True
        db.commit()
        db.refresh(lembrete)
        return lembrete

    def excluir(self, db: Session, id_lembrete: int) -> bool:
        lembrete = self.obter_por_id(db, id_lembrete)
        if not lembrete:
            return False

        db.delete(lembrete)
        db.commit()
        return True
    
    def obter_por_id(self, db: Session, id_lembrete: int) -> Lembrete | None:
        return db.query(Lembrete).filter(Lembrete.id_lembrete == id_lembrete).first()

    def obter_por_usuario(self, db: Session, id_usuario: int):
        return db.query(Lembrete).filter(Lembrete.id_usuario == id_usuario).all()



lembrete_crud = CRUDLembrete()
