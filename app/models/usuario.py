from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String)
    password_hash = Column(String, nullable=False)
    rol = Column(String)
    ubicacion_id = Column(Integer, ForeignKey("ubicacion.id"), nullable=True)

    ubicacion = relationship("Ubicacion", back_populates="usuarios")
    publicaciones = relationship("Publicacion", back_populates="usuario")
    donaciones = relationship("Donacion", back_populates="usuario")