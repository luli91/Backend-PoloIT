from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.models.estado import Estado, EstadoNombreEnum


def cargar_categorias(db: Session):
    categorias = ["Ropa", "Libros", "Muebles", "Alimentos", "Servicios", "Electrónica", "Juguetes"]
    
    for nombre in categorias:
        ya_existe = db.query(Categoria).filter_by(nombre=nombre).first()
        if not ya_existe:
            db.add(Categoria(nombre=nombre))
    
    db.commit()


def cargar_estados(db: Session):
    for estado_enum in EstadoNombreEnum:
        ya_existe = db.query(Estado).filter_by(nombre=estado_enum.value).first()
        if not ya_existe:
            db.add(Estado(nombre=estado_enum.value))
    
    db.commit()