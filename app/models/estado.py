from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum

class EstadoNombreEnum(str, Enum):
    pendiente = "Pendiente"
    entregado = "Entregado"
    cancelado = "Cancelado"

class Estado(Base):
    __tablename__ = "estado"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)

    publicaciones = relationship("Publicacion", back_populates="estado") 