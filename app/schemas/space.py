from pydantic import BaseModel


class SpaceCreate(BaseModel):
    """Datos necesarios para crear un espacio."""

    name: str
