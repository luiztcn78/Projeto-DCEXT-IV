from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash

class CRUDUsuario:
    def criar(self, db: Session, data: UsuarioCreate) -> Usuario:
        usuario = Usuario(
            nome=data.nome,
            email=data.email,
            tipo=data.tipo,
            senha=get_password_hash(data.senha),
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    def obter_por_email(self, db: Session, email: str):
        return db.query(Usuario).filter(Usuario.email == email).first()

    def obter_por_id(self, db: Session, id_usuario: int):
        return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

usuario_crud = CRUDUsuario()