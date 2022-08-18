"""Modelos utilizados para el dominio"""

from datetime import datetime
from pydantic import BaseModel
from enum import Enum

from .exceptions import SaldoInsuficiente


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

    def impacto(self) -> float:
        return self.importe if self.tipo == TipoMovimiento.INGRESO else -self.importe       

class Movimiento(MovimientoBase):
    id: int

    class Config:
        orm_mode = True

    @classmethod
    def crear_desde_db(cls, db_movimiento):
        return Movimiento(
            id=db_movimiento.id,
            id_cuenta=db_movimiento.id_cuenta,
            tipo=TipoMovimiento(db_movimiento.tipo),
            importe=db_movimiento.importe,
            fecha=db_movimiento.fecha
        ) 

class CrearMovimiento(MovimientoBase):
    pass

class Cuenta(BaseModel):
    """Modelo base de cuenta"""
    id: int
    id_cliente: int
    movimientos: list[Movimiento] = []

    class Config:
        orm_mode = True

    @classmethod
    def crear_desde_db(cls, db_cuenta):
        return Cuenta(
            id=db_cuenta.id,
            id_cliente=db_cuenta.id_cliente,
            movimientos=[
                Movimiento.crear_desde_db(movimiento)
                for movimiento in db_cuenta.movimientos
            ]
        )
    
    def saldo(self) -> float:
        return sum([movimiento.impacto() for movimiento in self.movimientos])
    
    def agregar_movimiento(self, moviemiento: Movimiento):
        if self.saldo() + moviemiento.impacto() < 0:
            raise SaldoInsuficiente
        else:
            self.movimientos.append(moviemiento)


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
