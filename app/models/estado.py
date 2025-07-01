from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.estado_nombre import EstadoNombreEnum

class Estado(Base):
    __tablename__ = "estado"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Enum(EstadoNombreEnum), nullable=False)

    publicaciones = relationship("Publicacion", back_populates="estado")
