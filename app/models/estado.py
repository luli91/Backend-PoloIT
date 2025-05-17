from sqlalchemy import Column, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum

class EstadoNombreEnum(str, Enum):
    Activo = "Activo"
    Entregado = "Entregado"
    Cancelado = "Cancelado"

class Estado(Base):
    __tablename__ = "estado"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(SQLEnum(EstadoNombreEnum, name="estado_enum"), unique=True, nullable=False)

    publicaciones = relationship("Publicacion", back_populates="estado")