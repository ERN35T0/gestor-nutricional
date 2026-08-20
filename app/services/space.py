from sqlalchemy.orm import Session

from app.models.space import Space
from app.schemas.space import SpaceCreate, SpaceUpdate


def create_space(db: Session, space: SpaceCreate):
    """
    Crea un espacio y lo guarda en la base de datos.
    """

    db_space = Space(
        name=space.name
    )

    db.add(db_space)
    db.commit()
    db.refresh(db_space)

    return db_space


def get_spaces(db: Session):
    """
    Devuelve todos los espacios almacenados.
    """

    return db.query(Space).all()


def get_space(db: Session, space_id: int):
    """
    Obtiene un espacio por su id.
    """

    return (
        db.query(Space)
        .filter(Space.id == space_id)
        .first()
    )


def update_space(
    db: Session,
    space_id: int,
    space: SpaceUpdate
):
    """
    Actualiza un espacio existente.
    """

    db_space = (
        db.query(Space)
        .filter(Space.id == space_id)
        .first()
    )

    if db_space is None:
        return None

    db_space.name = space.name

    db.commit()
    db.refresh(db_space)

    return db_space
