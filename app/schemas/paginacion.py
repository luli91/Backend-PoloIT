from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    total: int               # Total de registros (sin paginar)
    page: int                # Página actual (comienza en 1)
    per_page: int            # Cantidad por página
    pages: int               # Total de páginas
    has_next: bool           # ¿Hay una página siguiente?
    has_prev: bool           # ¿Hay una página anterior?
    items: List[T]           # Lista de ítems (paginados)
