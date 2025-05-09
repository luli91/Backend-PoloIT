from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Ubicacion(Base):
    __tablename__ = "ubicacion"

    id = Column(Integer, primary_key=True, index=True)
    direccion = Column(String)
    codigo_postal = Column(String)
    ciudad = Column(String)
    provincia = Column(String)

    usuarios = relationship("Usuario", back_populates="ubicacion")


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String, unique=True, index=True)
    telefono = Column(String)
    password_hash = Column(String)
    rol = Column(String)
    ubicacion_id = Column(Integer, ForeignKey("ubicacion.id"))

    ubicacion = relationship("Ubicacion", back_populates="usuarios")
    donaciones = relationship("Donacion", back_populates="usuario")


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)

    donaciones = relationship("Donacion", back_populates="categoria")


class Estado(Base):
    __tablename__ = "estado"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)

    donaciones = relationship("Donacion", back_populates="estado")


class Donacion(Base):
    __tablename__ = "donacion"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    cantidad = Column(Float)
    imagen_url = Column(String)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    categoria_id = Column(Integer, ForeignKey("categoria.id"))
    estado_id = Column(Integer, ForeignKey("estado.id"))

    usuario = relationship("Usuario", back_populates="donaciones")
    categoria = relationship("Categoria", back_populates="donaciones")
    estado = relationship("Estado", back_populates="donaciones")

