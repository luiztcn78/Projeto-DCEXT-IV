from sqlalchemy.orm import Session
from app.models.diario import Diario
from app.schemas.diario import DiarioCreate, DiarioUpdate
from datetime import datetime 

class CRUDDiario:
    def criar(self, db: Session, data: DiarioCreate):
        novo_diario = Diario(
            id_usuario=data.id_usuario,
            texto=data.texto,
            emocao=data.emocao,
            data_registro=datetime.now()
        )
        db.add(novo_diario)
        db.commit()
        db.refresh(novo_diario)
        return novo_diario

    def obter_por_id(self, db: Session, id_diario: int):
        return db.query(Diario).filter(Diario.id_diario == id_diario).first()

    def listar_por_usuario(self, db: Session, id_usuario: int):
        return db.query(Diario).filter(Diario.id_usuario == id_usuario).all()

    def atualizar(self, db: Session, id_diario: int, data: DiarioUpdate):
        diario = db.query(Diario).filter(Diario.id_diario == id_diario).first()
        if not diario:
            return None
        
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(diario, key, value)

        db.commit()
        db.refresh(diario)
        return diario

    def deletar(self, db: Session, id_diario: int):
        diario = db.query(Diario).filter(Diario.id_diario == id_diario).first()
        if not diario:
            return None
        
        db.delete(diario)
        db.commit()
        return diario


diario_crud = CRUDDiario()
