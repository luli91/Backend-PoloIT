from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum

class EstadoNombreEnum(str, Enum):
    pendiente = "pendiente"
    entregado = "entregado"
    cancelado = "cancelado"

class Estado(Base):
    __tablename__ = "estado"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(SQLEnum(EstadoNombreEnum, name="estado_enum"), unique=True)

    donaciones = relationship("Donacion", back_populates="estado")