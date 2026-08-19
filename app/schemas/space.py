from pydantic import BaseModel


class SpaceCreate(BaseModel):
    """Datos necesarios para crear un espacio."""

    name: str


class SpaceResponse(BaseModel):
    """
    Datos devueltos por la API.
    """

    id: int
    name: str

    class Config:
        from_attributes = True
