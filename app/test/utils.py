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