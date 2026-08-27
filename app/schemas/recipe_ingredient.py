from pydantic import BaseModel, ConfigDict


class RecipeIngredientCreate(BaseModel):
    """
    Datos necesarios para añadir un ingrediente a una receta.
    """

    recipe_id: int
    product_id: int
    quantity: float | None = None
    unit: str | None = None


class RecipeIngredientUpdate(BaseModel):
    """
    Datos permitidos para actualizar un ingrediente de una receta.
    """

    quantity: float | None = None
    unit: str | None = None


class RecipeIngredientResponse(BaseModel):
    """
    Datos de un ingrediente de receta devueltos por la API.
    """

    id: int
    recipe_id: int
    product_id: int
    quantity: float | None = None
    unit: str | None = None

    model_config = ConfigDict(from_attributes=True)
