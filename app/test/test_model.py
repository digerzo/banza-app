import pytest
from app import orm
from app.model import *


@pytest.fixture(name="movimientos")
def fixture_movimientos():
    return [
        Movimiento(id=1, id_cuenta=1, tipo=TipoMovimiento.INGRESO, importe=1000, fecha=datetime.now()),
        Movimiento(id=2, id_cuenta=1, tipo=TipoMovimiento.EGRESO, importe=100, fecha=datetime.now())
    ]

def test_crear_modelo_completo():
    movimiento = Movimiento(
        id=1,
        id_cuenta=2,
        tipo="INGRESO",
        importe=1000.0,
        fecha=datetime.now()
    )

    categoria = Categoria(id=1, nombre="Gold")

    cuenta = Cuenta(id=1, id_cliente=1, movimientos=[movimiento])

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

def test_crear_cuenta_desde_db():
    db_movimiento = orm.Movimiento(id=1, id_cuenta=1, tipo="INGRESO", importe=1000.0, fecha=datetime.now())
    db_cuenta = orm.Cuenta(id=1, id_cliente=1, movimientos=[db_movimiento])
    cuenta = Cuenta.crear_desde_db(db_cuenta)
    assert isinstance(cuenta, Cuenta)
    assert len(cuenta.movimientos) == 1

def test_saldo_cuenta(movimientos):
    cuenta = Cuenta(id=1, id_cliente=1, movimientos=movimientos)
    assert cuenta.saldo() == 900.0

def test_agregar_movimiento(movimientos):
    mov = Movimiento(id=1, id_cuenta=1, tipo=TipoMovimiento.EGRESO, importe=140, fecha=datetime.now())
    cuenta = Cuenta(id=1, id_cliente=1, movimientos=movimientos)
    cuenta.agregar_movimiento(mov)
    assert cuenta.saldo() == 760.0

def test_agregar_movimiento_saldo_insuficiente(movimientos):
    mov = Movimiento(id=1, id_cuenta=1, tipo=TipoMovimiento.EGRESO, importe=14000, fecha=datetime.now())
    cuenta = Cuenta(id=1, id_cliente=1, movimientos=movimientos)
    
    with pytest.raises(SaldoInsuficiente) as err:
        cuenta.agregar_movimiento(mov)
    
    assert cuenta.saldo() == 900.0
