from pydantic import BaseModel, ConfigDict


class RecipeCreate(BaseModel):
    """
    Datos necesarios para crear una receta.
    """

    name: str


class RecipeUpdate(BaseModel):
    """
    Datos permitidos para actualizar una receta.
    """

    name: str


class RecipeResponse(BaseModel):
    """
    Datos devueltos por la API.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
