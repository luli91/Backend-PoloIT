from fastapi import APIRouter, Depends, HTTPException
# queda para mas adelante -- from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, selectinload

# base de datos
from app.database import get_db

# modelos y esquemas
from app.models.usuario import Usuario
from app.models.ubicacion import Ubicacion
from app.schemas.usuario import UsuarioCreate, UsuarioOut, LoginRequest, TokenResponse

# hashing de contraseñas
from app.auth.hashing import hash_password, verificar_password

# JWT y autenticación
from app.auth.jwt import crear_token_acceso, solo_admin, obtener_usuario_actual

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

# Registro de nuevo usuario
@router.post("/registro", response_model=UsuarioOut)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya está en uso
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Crear ubicación primero
    nueva_ubicacion = Ubicacion(
        direccion=usuario.direccion,
        codigo_postal=usuario.codigo_postal,
        ciudad=usuario.ciudad,
        provincia=usuario.provincia
    )
    db.add(nueva_ubicacion)
    db.commit()
    db.refresh(nueva_ubicacion)

    # Crear usuario usando ubicacion_id generado
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        telefono=usuario.telefono,
        password_hash=hash_password(usuario.password),
        rol=usuario.rol,
        ubicacion_id=nueva_ubicacion.id
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
def leer_usuario_actual(usuario_actual: Usuario = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    usuario = db.query(Usuario)\
        .options(selectinload(Usuario.ubicacion))\
        .filter(Usuario.id == usuario_actual.id)\
        .first()
    return usuario

# Obtener lista completa de usuarios (solo admin)
@router.get("/", response_model=list[UsuarioOut])
def listar_usuarios(admin: Usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return db.query(Usuario).options(selectinload(Usuario.ubicacion)).all()

# Obtener usuario por ID
@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(
    usuario_id: int,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    # Solo el mismo usuario o un admin puede ver los datos
    if usuario_actual.id != usuario_id and usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso no autorizado")

    usuario = db.query(Usuario)\
        .options(selectinload(Usuario.ubicacion))\
        .filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

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
