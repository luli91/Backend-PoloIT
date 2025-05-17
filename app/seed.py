from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.models.estado import Estado, EstadoNombreEnum
from app.database import SessionLocal

def cargar_categorias(db: Session):
    ya_existen = db.query(Categoria).count()
    if ya_existen > 0:
        return

    categorias = [
        "Ropa", "Libros", "Muebles", "Alimentos",
        "Servicios", "Electrónica", "Juguetes"
    ]

    for nombre in categorias:
        db.add(Categoria(nombre=nombre))

    db.commit()

def cargar_estados(db: Session):
    ya_existen = db.query(Estado).count()
    if ya_existen > 0:
        return

    for estado_enum in EstadoNombreEnum:
        db.add(Estado(nombre=estado_enum.value))

    db.commit()

# Permite ejecutar el seed directamente con: python app/seed.py
if __name__ == "__main__":
    db = SessionLocal()
    cargar_estados(db)
    cargar_categorias(db)
    db.close()