from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from app.database import Base


class Donacion(Base):
    __tablename__ = "donacion"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)

    publicaciones = relationship("Publicacion", back_populates="donacion")
    usuario = relationship("Usuario", back_populates="donaciones")
    categoria = relationship("Categoria", back_populates="donaciones")

    @hybrid_property
    def tiene_publicacion(self) -> bool:
        return len(self.publicaciones) > 0
