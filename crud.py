from sqlalchemy.orm import Session
import models, schemas
from passlib.hash import bcrypt

def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = bcrypt.hash(usuario.password)
    db_usuario = models.Usuario(email=usuario.email, password_hash=hashed_password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario