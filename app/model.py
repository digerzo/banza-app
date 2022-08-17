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

    id: int
    nombre: str

    class Config:
        orm_mode = True


class MovimientoBase(BaseModel):
    """Modelo base de movimiento"""
    
    id_cuenta: int
    tipo: TipoMovimiento
    importe: float
    fecha: datetime

class Movimiento(MovimientoBase):
    id: int

    class Config:
        orm_mode = True


class CrearMovimiento(MovimientoBase):
    pass

class Cuenta(BaseModel):
    """Modelo base de cuenta"""

    movimientos: list[Movimiento] = []

    class Config:
        orm_mode = True


class ClienteBase(BaseModel):
    """Modelo base de cliente"""

    nombre: str

class CrearCliente(ClienteBase):
    pass

class Cliente(ClienteBase):

    id: int
    categorias: list[Categoria] = []
    cuentas: list[Cuenta] = []
    
    class Config:
        orm_mode = True

class AgregarClienteACategoria(BaseModel):
    categoria: str

class CuentaConSaldo(BaseModel):
    id_cuenta: int
    saldo: float
