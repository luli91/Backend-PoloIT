from sqlalchemy import Column, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.estado_nombre import EstadoNombre

class Estado(Base):
    __tablename__ = "estado"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(SQLEnum(EstadoNombre, name="estado_enum"), unique=True, nullable=False)

    publicaciones = relationship("Publicacion", back_populates="estado")