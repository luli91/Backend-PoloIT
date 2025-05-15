from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.ubicacion import Ubicacion

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String, unique=True)
    telefono = Column(String)
    password_hash = Column(String)
    rol = Column(String)
    ubicacion_id = Column(Integer, ForeignKey("ubicacion.id"), nullable=True)

    ubicacion = relationship("Ubicacion", back_populates="usuarios") 
    donaciones = relationship("Donacion", back_populates="usuario")