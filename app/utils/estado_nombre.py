from enum import Enum

class EstadoNombreEnum(str, Enum):
    Activo = "Activo"
    Entregado = "Entregado"
    Cancelado = "Cancelado"