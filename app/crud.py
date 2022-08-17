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

def get_categoria_nombre(db: Session, nombre_categoria: str):
    return db.query(orm.Categoria).filter(orm.Categoria.nombre == nombre_categoria).first()

def agregar_cliente_categoria(db: Session, cliente: orm.Cliente, categoria: orm.Categoria):
    cliente.categorias.append(categoria)
    db.commit()
    db.refresh(cliente)
    return cliente

def get_cuenta(db: Session, id_cuenta: int):
    return db.query(orm.Cuenta).filter(orm.Cuenta.id == id_cuenta).first()