from sqlalchemy.types import DateTime
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

    cuentas = relationship("Cuenta", back_populates="duenio")


class Cuenta(Base):
    __tablename__ = "cuentas"

    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"))

    duenio = relationship("Cliente", back_populates="cuentas")
    movimientos = relationship("Movimiento", back_populates="cuenta")

class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id"))
    tipo = Column(String)
    importe = Column(Float)
    fecha = Column(DateTime)

    cuenta = relationship("Cuenta", back_populates="movimientos")
