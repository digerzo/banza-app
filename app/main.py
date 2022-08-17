from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, model, orm
from .database import SessionLocal, engine

orm.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/clientes/")
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_clientes(db=db, skip=skip, limit=limit)


@app.get("/clientes/{id_cliente}", response_model=model.Cliente)
def obtener_cliente(id_cliente: int, db: Session = Depends(get_db)):
    return crud.get_cliente(db, id_cliente)


@app.post("/clientes/", response_model=model.Cliente)
def crear_cliente(cliente: model.CrearCliente, db: Session = Depends(get_db)):
    return crud.crear_cliente(db=db, cliente=cliente)
