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
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_clientes(popular_limpiar_db):
    response = client.get("/clientes/")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_cliente(popular_limpiar_db):
    ids = popular_limpiar_db
    id_cliente = ids[0]
    response = client.get("/clientes/" + str(id_cliente))
    assert response.status_code == 200
    assert response.json()["nombre"] == "carlos"


def test_get_cliente_not_found(popular_limpiar_db):
    random_id = 112233445566778899
    response = client.get("/clientes/" + str(random_id))
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente not found"


def test_crear_cliente(popular_limpiar_db):
    cliente = model.CrearCliente(nombre="Juan")
    response = client.post("/clientes/", data=cliente.json())
    assert response.status_code == 200
    assert response.json()["nombre"] == "Juan"
    assert isinstance(response.json()["id"], int)


def test_eliminar_cliente(popular_limpiar_db):
    id_eliminar = popular_limpiar_db[0]
    response = client.delete("/clientes/" + str(id_eliminar))
    assert response.status_code == 200
    response = client.get("/clientes/" + str(id_eliminar))
    assert response.status_code == 404


def test_eliminar_cliente_not_found(popular_limpiar_db):
    id_eliminar = 123123
    response = client.delete("/clientes/" + str(id_eliminar))
    assert response.status_code == 404


def test_agregar_cliente_a_categoria(popular_limpiar_db):
    id_cliente = popular_limpiar_db[0]
    agregar_categoria = model.AgregarClienteACategoria(categoria="Gold")
    response = client.post("/clientes/" + str(id_cliente) + "/categorias/", data=agregar_categoria.json())
    assert response.status_code == 200
    assert response.json()["categorias"][0]["nombre"] == "Gold" 


def test_agregar_cliente_a_categoria_cliente_not_found(popular_limpiar_db):
    id_cliente = 123123
    agregar_categoria = model.AgregarClienteACategoria(categoria="Gold")
    response = client.post("/clientes/" + str(id_cliente) + "/categorias/", data=agregar_categoria.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente not found"


def test_agregar_cliente_a_categoria_cliente_not_found(popular_limpiar_db):
    id_cliente = popular_limpiar_db[0]
    agregar_categoria = model.AgregarClienteACategoria(categoria="Platinum Super Black")
    response = client.post("/clientes/" + str(id_cliente) + "/categorias/", data=agregar_categoria.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "Categoria not found"


def test_consulta_cuentas_cliente(popular_limpiar_db):
    id_cliente = popular_limpiar_db[0]
    response = client.get(f"/clientes/{str(id_cliente)}/cuentas/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_consulta_cuentas_cliente_not_found():
    idc = 12345
    response = client.get(f"/clientes/{str(idc)}/cuentas/")
    assert response.status_code == 404
