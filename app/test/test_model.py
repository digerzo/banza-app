import pytest
from app.model import *

def test_crear_modelo_completo():
    movimiento = Movimiento(
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