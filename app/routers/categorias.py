from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaOut
from app.auth.jwt import solo_admin
from typing import List

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.get("/", response_model=List[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@router.post("/", response_model=CategoriaOut)
def crear_categoria(
    categoria: CategoriaCreate,
    admin = Depends(solo_admin),
    db: Session = Depends(get_db)
):
    nueva = Categoria(**categoria.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/{categoria_id}", response_model=CategoriaOut)
def actualizar_categoria(
    categoria_id: int,
    datos: CategoriaCreate,
    admin = Depends(solo_admin),
    db: Session = Depends(get_db)
):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    categoria.nombre = datos.nombre
    db.commit()
    db.refresh(categoria)
    return categoria

@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int,
    admin = Depends(solo_admin),
    db: Session = Depends(get_db)
):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(categoria)
    db.commit()
    return {"ok": True, "mensaje": "Categoría eliminada"}