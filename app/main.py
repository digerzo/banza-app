from http import client
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .adapter import ClientDolarSi

from .exceptions import SaldoInsuficiente

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


@app.get("/clientes/", response_model=list[model.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Proporciona una lista con todos los clientes disponibles"""
    return crud.get_clientes(db=db, skip=skip, limit=limit)


@app.get("/clientes/{id_cliente}", response_model=model.Cliente)
def obtener_cliente(id_cliente: int, db: Session = Depends(get_db)):
    """Obtiene un cliente en particular"""
    db_cliente = crud.get_cliente(db, id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente


@app.post("/clientes/", response_model=model.Cliente)
def crear_cliente(cliente: model.CrearCliente, db: Session = Depends(get_db)):
    """Crea un cliente, devolviendo el mismo"""
    return crud.crear_cliente(db=db, cliente=cliente)


@app.delete("/clientes/{id_cliente}")
def eliminar_cliente(id_cliente: int, db: Session = Depends(get_db)):
    """Elimina un cliente especifico"""
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
    """Agrega un cliente a la categoria deseada"""
    db_cliente = crud.get_cliente(db, id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    
    db_categoria = crud.get_categoria_nombre(db, agregar_categoria.categoria)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria not found")
        
    return crud.agregar_cliente_categoria(db, db_cliente, db_categoria)


@app.get("/clientes/{id_cliente}/cuentas/", response_model=list[model.Cuenta])
def read_cliente_cuentas(id_cliente: int, db: Session = Depends(get_db)):
    """Obtiene las cuentas de un cliente"""
    db_cliente = crud.get_cliente(db, id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    
    return db_cliente.cuentas


@app.get("/clientes/{id_cliente}/cuentas/{id_cuenta}/saldo/", response_model=model.CuentaConSaldo)
def consultar_saldo_cuenta_cliente(id_cliente: int, id_cuenta: int, db: Session = Depends(get_db)):
    """Obtiene el saldo de una cuenta de un cliente"""
    db_cliente = crud.get_cliente(db, id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    
    db_cuenta = crud.get_cuenta(db, id_cuenta)
    if db_cuenta is None:
        raise HTTPException(status_code=404, detail="Cuenta not found")

    cuenta = model.Cuenta.crear_desde_db(db_cuenta)
    
    return model.CuentaConSaldo(id_cuenta=db_cuenta.id, saldo=cuenta.saldo())


@app.post("/movimientos/", response_model=model.Movimiento)
def registrar_movimiento(movimiento: model.CrearMovimiento, db: Session = Depends(get_db)):
    """Registra un nuevo movimiento"""
    db_cuenta = crud.get_cuenta(db, movimiento.id_cuenta)
    if db_cuenta is None:
        raise HTTPException(status_code=404, detail="Cuenta not found")

    cuenta = model.Cuenta.crear_desde_db(db_cuenta)
    try:
        cuenta.agregar_movimiento(movimiento)
    except SaldoInsuficiente as e:
        raise HTTPException(status_code=409, detail="Saldo insuficiente") from e
    
    return crud.crear_movimiento(db, movimiento)


@app.get("/movimientos/{id_movimiento}", response_model=model.Movimiento)
def consultar_movimiento(id_movimiento: int, db: Session = Depends(get_db)):
    """Obtiene un movimiento especifico"""
    db_movimiento = crud.get_movimiento(db, id_movimiento)
    if db_movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento not found")

    return db_movimiento


@app.delete("/movimientos/{id_movimiento}")
def eliminar_movimiento(id_movimiento: int, db: Session = Depends(get_db)):
    """Elimina un movimiento especifico"""
    db_movimiento = crud.get_movimiento(db, id_movimiento)
    if db_movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento not found")
    
    return crud.eliminar_movimiento(db, db_movimiento)


@app.get("/cotizacion/")
def get_cotizacion_dolar_bolsa():
    """Test endpoint para probar obtener la cotizacion Dolar Bolsa de """
    client = ClientDolarSi()
    cotizacion = client.get_cotizacion_dolar_bolsa()
    return {"venta_dolar_bolsa": cotizacion}


@app.get("/iniciardb/")
def inicializar_db(db: Session = Depends(get_db)):
    """Endpoint de testing para inicializar la db"""
    categorias = [
        orm.Categoria(id=1, nombre="Bronce"),
        orm.Categoria(id=2, nombre="Silver"),
        orm.Categoria(id=3, nombre="Gold")
    ]
    for cat in categorias:
        db.add(cat)
    db.commit()
    cliente = orm.Cliente(id=100, nombre="Agustin", categorias=[categorias[0]])
    db.add(cliente)
    db.commit()
    cuenta = orm.Cuenta(id=100, id_cliente=100)
    db.add(cuenta)
    db.commit()
    return {"resultado": "ok"}
