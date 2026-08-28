from pydantic import BaseModel, ConfigDict


class MealSuggestionCreate(BaseModel):
    """
    Datos necesarios para crear una sugerencia de comida.
    """

    meal_slot_id: int
    prepared_meal_id: int


class MealSuggestionResponse(BaseModel):
    """
    Datos de una sugerencia de comida devueltos por la API.
    """

    id: int
    meal_slot_id: int
    prepared_meal_id: int

    model_config = ConfigDict(from_attributes=True)
