import pytest
from app import orm
from app.model import *

def test_crear_modelo_completo():
    movimiento = Movimiento(
        id=1,
        id_cuenta=2,
        tipo="INGRESO",
        importe=1000.0,
        fecha=datetime.now()
    )

    categoria = Categoria(id=1, nombre="Gold")

    cuenta = Cuenta(movimientos=[movimiento])

    cliente = Cliente(
        id=1,
        nombre="Juan",
        categorias=[categoria],
        cuentas=[cuenta]
    )

    assert len(cliente.categorias) == 1


def test_crear_movimiento_desde_db():
    db_movimiento = orm.Movimiento(
        id=1, id_cuenta=1, tipo="INGRESO", importe=1000.0, fecha=datetime.now()
    )
    movimiento = Movimiento.crear_desde_db(db_movimiento)
    assert isinstance(movimiento, Movimiento)
    assert movimiento.tipo.value == "INGRESO"