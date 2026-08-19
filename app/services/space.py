from sqlalchemy.orm import Session

from app.models.space import Space
from app.schemas.space import SpaceCreate


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
