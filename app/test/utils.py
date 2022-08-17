from datetime import date, datetime
from app import orm

def popular_clientes(session) -> list[int]:
    clientes = [
        orm.Cliente(nombre="carlos"),
        orm.Cliente(nombre="alberto"),
        orm.Cliente(nombre="saul"),
    ]
    
    for cliente in clientes:
        session.add(cliente)
    session.commit()
    return [cliente.id for cliente in clientes]


def limpiar_clientes(session):
    session.execute("delete from clientes")
    session.commit()


def popular_categorias(db):
    categorias = [
        orm.Categoria(nombre="Bronce"),
        orm.Categoria(nombre="Silver"),
        orm.Categoria(nombre="Gold"),
    ]
    for c in categorias:
        db.add(c)
    db.commit()

def limpiar_categorias(db):
    cats = db.query(orm.Categoria).all()
    for c in cats:
        db.delete(c)
    db.commit()


def popular_cuentas(db, id_cliente):
    cuentas = [
        orm.Cuenta(id_cliente=id_cliente),
        orm.Cuenta(id_cliente=id_cliente)
        ]
    for c in cuentas:
        db.add(c)
    db.commit()
    cuenta = cuentas[0]
    db.refresh(cuenta)
    cuenta.movimientos.append(
        orm.Movimiento(id_cuenta=cuenta.id, tipo="INGRESO", importe=10500, fecha=datetime.now())
    )   
    cuenta.movimientos.append(
        orm.Movimiento(id_cuenta=cuenta.id, tipo="EGRESO", importe=604.50, fecha=datetime.now())
    )   

    db.commit()


def limpiar_cuentas(db):
    cuentas = db.query(orm.Cuenta).all()
    for c in cuentas:
        for m in c.movimientos:
            db.delete(m)
        db.delete(c)
    db.commit()

