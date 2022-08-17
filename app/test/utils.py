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