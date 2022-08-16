"""Modelos utilizados para el dominio"""

from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class TipoMovimiento(Enum):
    """Tipos de movimiento asociados a una cuenta"""

    EGRESO = "EGRESO"
    INGRESO = "INGRESO"   



class Categoria(BaseModel):
    """Modelo base de categoría"""

    nombre: str


class Movimiento(BaseModel):
    """Modelo base de movimiento"""
    
    tipo: TipoMovimiento
    importe: float
    fecha: datetime


class Cuenta(BaseModel):
    """Modelo base de cuenta"""

    movimientos: list[Movimiento] = []

class Cliente(BaseModel):
    """Modelo base de cliente"""

    nombre: str
    categorias: list[Categoria] = []
    cuentas: list[Cuenta] = []
