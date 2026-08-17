from app.models.space import Space
from app.schemas.space import SpaceCreate


def create_space(space: SpaceCreate) -> Space:
    """Crea un Space a partir de los datos validados de entrada."""
    return Space(name=space.name)
