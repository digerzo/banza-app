from fastapi import Depends, FastAPI, HTTPException
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
    db_cliente = crud.get_cliente(db, id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente


@app.post("/clientes/", response_model=model.Cliente)
def crear_cliente(cliente: model.CrearCliente, db: Session = Depends(get_db)):
    return crud.crear_cliente(db=db, cliente=cliente)


@app.delete("/clientes/{id_cliente}")
def eliminar_cliente(id_cliente: int, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return crud.eliminar_cliente(db, db_cliente)


@app.post("/clientes/{id_cliente}/categorias/", response_model=model.Cliente)
def agregar_cliente_categoria(
            id_cliente: int, 
            agregar_categoria: model.AgregarClienteACategoria, 
            db: Session = Depends(get_db)
        ):
    db_cliente = crud.get_cliente(db, id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    
    db_categoria = crud.get_categoria_nombre(db, agregar_categoria.categoria)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria not found")
        
    return crud.agregar_cliente_categoria(db, db_cliente, db_categoria)


@app.get("/clientes/{id_cliente}/cuentas/", response_model=list[model.Cuenta])
def read_cliente_cuentas(id_cliente: int, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    
    return db_cliente.cuentas