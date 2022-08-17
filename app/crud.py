from sqlalchemy.orm import Session

from . import orm, model


def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(orm.Cliente).offset(skip).limit(limit).all()

def get_cliente(db: Session, user_id: int):
    return db.query(orm.Cliente).filter(orm.Cliente.id == user_id).first()

def crear_cliente(db: Session, cliente: model.CrearCliente) -> orm.Cliente:
    db_cliente = orm.Cliente(nombre=cliente.nombre)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def eliminar_cliente(db: Session, cliente: orm.Cliente):
    db.delete(cliente)
    db.commit()