from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.usuario import Usuario

load_dotenv()

# Variables de entorno
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))

# OAuth2PasswordBearer para proteger endpoints
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

# Crear token JWT
def crear_token_acceso(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verificar token y decodificar payload
def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Dependencia para obtener sesión a la base
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Obtener usuario autenticado desde el token
def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    usuario_id = int(payload.get("sub"))
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario

def solo_admin(usuario: Usuario = Depends(obtener_usuario_actual)) -> Usuario:
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso solo permitido para administradores")
    return usuario