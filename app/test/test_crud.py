import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import crud, model, orm
from .utils import popular_clientes, limpiar_clientes

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

orm.Base.metadata.create_all(bind=engine)

@pytest.fixture(name="session")
def fixture_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_get_cliente_por_id(session):
    db_cliente = orm.Cliente(nombre="carlos")
    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)

    rows = list(session.execute("select nombre from clientes"))
    assert rows == [("carlos",)]

    cliente = crud.get_cliente(session, db_cliente.id)
    assert cliente == db_cliente
    
    limpiar_clientes(session)


def test_crear_cliente(session):
    cliente = model.CrearCliente(nombre="carlos")
    _ = crud.crear_cliente(session, cliente)
    rows = list(session.execute("select nombre from clientes"))

    assert rows == [("carlos",)]

    limpiar_clientes(session)


def test_read_clientes(session):
    popular_clientes(session)
    
    clientes = crud.get_clientes(session)

    assert len(clientes) == 3

    limpiar_clientes(session)