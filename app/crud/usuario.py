from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


class CRUDUsuario:

    def criar(self, db: Session, data: UsuarioCreate) -> Usuario:
        usuario = Usuario(
            nome=data.nome,
            email=data.email,
            tipo=data.tipo,
            senha=data.senha,  # senha “normal”, sem hash
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    def obter_por_email(self, db: Session, email: str):
        return db.query(Usuario).filter(Usuario.email == email.strip()).first()

    def obter_por_id(self, db: Session, id_usuario: int):
        return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    
    def listar_com_limit(self, db: Session, limit: int = 10):
        return db.query(Usuario).limit(limit).all()
    
    def atualizar(self, db: Session, id_usuario: int, data: UsuarioUpdate) -> Usuario | None:
        usuario = self.obter_por_id(db, id_usuario)
        if not usuario:
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(usuario, key, value)

        db.commit()
        db.refresh(usuario)
        return usuario
    
    def excluir(self, db: Session, id_usuario: int) -> bool:
        usuario = self.obter_por_id(db, id_usuario)
        if not usuario:
            return False

        db.delete(usuario)
        db.commit()
        return True

usuario_crud = CRUDUsuario()