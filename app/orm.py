from sqlalchemy.types import DateTime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table, Enum
from sqlalchemy.orm import relationship

from .model import TipoMovimiento
from .database import Base


categoria_cliente = Table(
    "categoria_cliente",
    Base.metadata,
    Column("id_cliente", ForeignKey("clientes.id"), primary_key=True),
    Column("id_categoria", ForeignKey("categorias.id"), primary_key=True),
)

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

    categorias = relationship("Categoria", secondary=categoria_cliente)
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
    tipo = Column(Enum(TipoMovimiento))
    importe = Column(Float)
    fecha = Column(DateTime)

    cuenta = relationship("Cuenta", back_populates="movimientos")

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
