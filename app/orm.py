from xmlrpc.client import DateTime
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry, relationship

from .model import Cliente, Cuenta, Movimiento

mapper_registry = registry()

tabla_cliente = Table(
    'cliente',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('nombre', String(50)),
)

tabla_cuenta = Table(
    'cuenta',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('id_cliente', Integer, ForeignKey('cliente.id'))
)

tabla_movimiento = Table(
    'movimiento',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('id_cuenta', Integer, ForeignKey('cuenta.id')),
    Column('tipo', String(50)),
    Column('fecha', DateTime),
)

def start_mapers():

    mapper_registry.map_imperatively(Cliente, tabla_cliente, properties={
        'cuentas' : relationship(Cuenta, backref='cliente', order_by=tabla_cuenta.c.id)
    })

    mapper_registry.map_imperatively(Cuenta, tabla_cuenta, properties={
        'movimientos' : relationship(Movimiento, backref='cuenta', order_by=tabla_movimiento.c.id)
    })

    mapper_registry.map_imperatively(Movimiento, tabla_movimiento)

