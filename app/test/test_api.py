from datetime import datetime
from pdb import Pdb
from urllib import response
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app import model, orm
from app.main import app, get_db
from . import utils

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
orm.Base.metadata.create_all(bind=engine)
client = TestClient(app)


@pytest.fixture(name="popular_limpiar_db")
def fixture_popular_limpiar_db():
    """Fixture para inicializar y limpiar la base de datos"""
    db = TestingSessionLocal()
    utils.popular_categorias(db)
    ids = utils.popular_clientes(db)
    utils.popular_cuentas(db, ids[0])
    yield ids
    utils.limpiar_cuentas(db)
    utils.limpiar_clientes(db)
    utils.limpiar_categorias(db)
    db.close()


def test_read_main():
    """Test hello world"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_clientes(popular_limpiar_db):
    """Test consultar todos los clientes cuando tengo data en la db"""
    response = client.get("/clientes/")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_cliente(popular_limpiar_db):
    """Test obtener un cliente especifico cuando tengo data en la db"""
    ids = popular_limpiar_db
    id_cliente = ids[0]
    response = client.get("/clientes/" + str(id_cliente))
    assert response.status_code == 200
    assert response.json()["nombre"] == "carlos"


def test_get_cliente_not_found(popular_limpiar_db):
    """Test tratar obtener un cliente que no existe me devuelve 404"""
    random_id = 112233445566778899
    response = client.get("/clientes/" + str(random_id))
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente not found"


def test_crear_cliente(popular_limpiar_db):
    """Test crear un cliente"""
    cliente = model.CrearCliente(nombre="Juan")
    response = client.post("/clientes/", data=cliente.json())
    assert response.status_code == 200
    assert response.json()["nombre"] == "Juan"
    assert isinstance(response.json()["id"], int)


def test_eliminar_cliente(popular_limpiar_db):
    """Test eliminar un cliente dado que tengo clientes en la db"""
    id_eliminar = popular_limpiar_db[0]
    response = client.delete("/clientes/" + str(id_eliminar))
    assert response.status_code == 200
    response = client.get("/clientes/" + str(id_eliminar))
    assert response.status_code == 404


def test_eliminar_cliente_not_found(popular_limpiar_db):
    """Test eliminar un cliente que no existe me devuelve 404"""
    id_eliminar = 123123
    response = client.delete("/clientes/" + str(id_eliminar))
    assert response.status_code == 404


def test_agregar_cliente_a_categoria(popular_limpiar_db):
    """Test agregar a un cliente a una categoria que existe"""
    id_cliente = popular_limpiar_db[0]
    agregar_categoria = model.AgregarClienteACategoria(categoria="Gold")
    response = client.post("/clientes/" + str(id_cliente) + "/categorias/", data=agregar_categoria.json())
    assert response.status_code == 200
    assert response.json()["categorias"][0]["nombre"] == "Gold" 


def test_agregar_cliente_a_categoria_cliente_not_found(popular_limpiar_db):
    """Test agregar un cliente que no existe a una categoria me devuelve 404"""
    id_cliente = 123123
    agregar_categoria = model.AgregarClienteACategoria(categoria="Gold")
    response = client.post("/clientes/" + str(id_cliente) + "/categorias/", data=agregar_categoria.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente not found"


def test_agregar_cliente_a_categoria_categoria_not_found(popular_limpiar_db):
    """Test agregar cliente a una categoria que no existe me devuelve 404"""
    id_cliente = popular_limpiar_db[0]
    agregar_categoria = model.AgregarClienteACategoria(categoria="Platinum Super Black")
    response = client.post("/clientes/" + str(id_cliente) + "/categorias/", data=agregar_categoria.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "Categoria not found"


def test_consulta_cuentas_cliente(popular_limpiar_db):
    """Test obtener las cuentas de un cliente cuando tengo data en la db"""
    id_cliente = popular_limpiar_db[0]
    response = client.get(f"/clientes/{str(id_cliente)}/cuentas/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_consulta_cuentas_cliente_not_found():
    """Test consultar las cuentas de un cliente que no existe me devuelve 404"""
    idc = 12345
    response = client.get(f"/clientes/{str(idc)}/cuentas/")
    assert response.status_code == 404


def test_get_saldo_cuenta_con_movimientos(popular_limpiar_db):
    """Test obtener el saldo de una cuenta cuando tengo data en la db"""
    id_cliente = popular_limpiar_db[0]
    id_cuenta = 1
    response = client.get(f"/clientes/{str(id_cliente)}/cuentas/{str(id_cuenta)}/saldo/")
    assert response.status_code == 200
    assert isinstance(response.json()["saldo"], float)


def test_get_saldo_cuenta_sin_movimientos(popular_limpiar_db):
    """Test obtener el saldo de una cuenta que no tiene movimientos deberia ser 0"""
    id_cliente = popular_limpiar_db[0]
    id_cuenta = 2
    response = client.get(f"/clientes/{str(id_cliente)}/cuentas/{str(id_cuenta)}/saldo/")
    assert response.status_code == 200
    assert isinstance(response.json()["saldo"], float)
    assert response.json()["saldo"] == 0


def test_get_saldo_cuenta_cliente_not_found(popular_limpiar_db):
    """Test obtener el saldo de un cliente o una cuenta que no existe me devuelve 404"""
    idc = 1234
    response = client.get(f"/clientes/{str(idc)}/cuentas/2/saldo/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente not found"

    id_cuenta = 91328
    response = client.get(f"/clientes/1/cuentas/{str(id_cuenta)}/saldo/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cuenta not found"


def test_registrar_movimiento(popular_limpiar_db):
    """Test registrar un nuevo movimiento tipo INGRESO funciona ok"""
    movimiento = model.CrearMovimiento(id_cuenta=1, tipo="INGRESO", importe=1000, fecha=datetime.now())
    response = client.post("/movimientos/", data=movimiento.json())
    assert response.status_code == 200
    assert isinstance(response.json()["id"], int)


def test_registrar_movimiento_saldo_insuficiente(popular_limpiar_db):
    """Test registrar un nuevo movimiento tipo EGRESO devuelve 409 cuando tengo saldo isuficiente"""
    movimiento = model.CrearMovimiento(id_cuenta=1, tipo="EGRESO", importe=99999, fecha=datetime.now())
    response = client.post("/movimientos/", data=movimiento.json())
    assert response.status_code == 409
    assert response.json()["detail"] == "Saldo insuficiente"


def test_registrar_movimiento_cuenta_not_found():
    """Test registrar un movimiento para una cuenta inexistente devuelve 404"""
    movimiento = model.CrearMovimiento(id_cuenta=1, tipo="INGRESO", importe=1000, fecha=datetime.now())
    response = client.post("/movimientos/", data=movimiento.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "Cuenta not found"


def test_consultar_movimiento(popular_limpiar_db):
    """Test consultar un movimiento en particular funciona ok"""
    id_movimiento = 1  # por la forma de llenar la db puedo asumir esto
    response = client.get(f"/movimientos/{id_movimiento}")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_consultar_movimiento_not_found():
    """Test consultar un movimiento que no existe devuelve 404"""
    id_movimiento = 1123
    response = client.get(f"/movimientos/{id_movimiento}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movimiento not found"


def test_eliminar_movimiento(popular_limpiar_db):
    """Test eliminar movimiento funciona ok"""
    id_movimiento = 1
    response = client.delete(f"/movimientos/{id_movimiento}")
    assert response.status_code == 200
    response = client.get(f"/moviemientos/{id_movimiento}")
    assert response.status_code == 404


def test_eliminar_movimiento_not_found():
    """Test eliminar un movimiento que no existe devuelve 404"""
    id_movimiento = 1
    response = client.delete(f"/movimientos/{id_movimiento}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movimiento not found"
