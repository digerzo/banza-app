import pytest
from sqlalchemy.orm import Session

from app import crud, model, orm
from app.database import SessionLocal, engine

orm.Base.metadata.create_all(bind=engine)

@pytest.fixture(name="session")
def fixture_session():
    db = SessionLocal()
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
    
    # work around por ahora
    session.execute("delete from clientes")
    session.commit()


def test_crear_cliente(session):
    cliente = model.CrearCliente(nombre="carlos")
    _ = crud.crear_cliente(session, cliente)
    rows = list(session.execute("select nombre from clientes"))

    assert rows == [("carlos",)]

    # work around por ahora
    session.execute("delete from clientes")
    session.commit()
    
    