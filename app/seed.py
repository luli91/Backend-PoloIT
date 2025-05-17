from sqlalchemy.orm import Session
from app.models.estado import Estado, EstadoNombreEnum
from app.models.categoria import Categoria
from app.database import SessionLocal

def cargar_estados(db: Session):
    print("Cargando estados...")
    if db.query(Estado).count() > 0:
        print("Ya existen estados, se omite carga.")
        return
    for estado in EstadoNombreEnum:
        db.add(Estado(nombre=estado))
    db.commit()
    print("Estados cargados correctamente.")

def cargar_categorias(db: Session):
    print("Cargando categorías...")
    categorias = [
        "Ropa", "Libros", "Muebles", "Alimentos",
        "Servicios", "Electrónica", "Juguetes"
    ]
    if db.query(Categoria).count() > 0:
        print("Ya existen categorías, se omite carga.")
        return
    for nombre in categorias:
        db.add(Categoria(nombre=nombre))
    db.commit()
    print("Categorías cargadas correctamente.")

# Permite correr el seed directamente
if __name__ == "__main__":
    db = SessionLocal()
    cargar_estados(db)
    cargar_categorias(db)
    db.close()