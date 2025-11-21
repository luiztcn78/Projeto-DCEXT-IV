from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.atividade import Atividade
from app.schemas.atividade import AtividadeCreate, AtividadeUpdate


class CRUDAtividade:

    def criar(self, db: Session, data: AtividadeCreate) -> Atividade:
        # Verifica se já existe uma atividade com o mesmo nome para o mesmo usuário
        atividade_existente = db.query(Atividade).filter(
            Atividade.id_usuario == data.id_usuario,
            Atividade.nome == data.nome.strip()
        ).first()

        if atividade_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma atividade com esse nome para este usuário."
            )

        atividade = Atividade(
            id_usuario=data.id_usuario,
            nome=data.nome.strip(),
            descricao=data.descricao,
            tipo=data.tipo,
            dias_da_semana=data.dias_da_semana,
            horario=data.horario,
            ativo=data.ativo if data.ativo is not None else True
        )

        db.add(atividade)
        db.commit()
        db.refresh(atividade)
        return atividade

    def atualizar(self, db: Session, id_atividade: int, data: AtividadeUpdate) -> Atividade | None:
        atividade = self.obter_por_id(db, id_atividade)
        if not atividade:
            return None

        update_data = data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(atividade, key, value)

        db.commit()
        db.refresh(atividade)
        return atividade

    def ativar_desativar(self, db: Session, id_atividade: int) -> Atividade | None:
        atividade = self.obter_por_id(db, id_atividade)
        if not atividade:
            return None

        atividade.ativo = not atividade.ativo
        db.commit()
        db.refresh(atividade)
        return atividade

    def excluir(self, db: Session, id_atividade: int) -> bool:
        atividade = self.obter_por_id(db, id_atividade)
        if not atividade:
            return False

        db.delete(atividade)
        db.commit()
        return True

    def listar_todas(self, db: Session, limit: int = 10):
        return (
        db.query(Atividade)
        .order_by(Atividade.id_atividade.desc())
        .limit(limit)
        .all()
    )

    def obter_por_id(self, db: Session, id_atividade: int) -> Atividade | None:
        return db.query(Atividade).filter(Atividade.id_atividade == id_atividade).first()

    def obter_por_usuario(self, db: Session, id_usuario: int):
        return db.query(Atividade).filter(Atividade.id_usuario == id_usuario).all()


atividade_crud = CRUDAtividade()
