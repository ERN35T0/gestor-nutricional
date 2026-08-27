from pydantic import BaseModel, ConfigDict


class SpaceCreate(BaseModel):
    """Datos necesarios para crear un espacio."""

    name: str


class SpaceUpdate(BaseModel):
    """Datos permitidos para actualizar un espacio."""

    name: str


class SpaceResponse(BaseModel):
    """
    Datos devueltos por la API.
    """

    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
