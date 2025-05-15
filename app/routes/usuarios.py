from fastapi import APIRouter, Depends, HTTPException
# queda para mas adelante -- from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# base de datos
from app.database import SessionLocal

# modelos y esquemas
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut, LoginRequest, TokenResponse

# hashing de contraseñas
from app.auth.hashing import hash_password, verificar_password

# JWT y autenticación
from app.auth.jwt import crear_token_acceso, solo_admin, obtener_usuario_actual

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Registro de nuevo usuario
@router.post("/registro", response_model=UsuarioOut)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        telefono=usuario.telefono,
        rol=usuario.rol,
        password_hash=hash_password(usuario.password),
        ubicacion_id=usuario.ubicacion_id,
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# Login de usuario (devuelve token JWT)
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    if not usuario or not verificar_password(request.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = crear_token_acceso({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer"}

# Obtener usuario actual
@router.get("/me", response_model=UsuarioOut)
def leer_usuario_actual(usuario: Usuario = Depends(obtener_usuario_actual)):
    return usuario


# Borrar usuario (solo admin)
@router.delete("/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    admin: Usuario = Depends(solo_admin), # Dependencia para verificar si el usuario es admin
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"ok": True, "mensaje": "Usuario eliminado"}
