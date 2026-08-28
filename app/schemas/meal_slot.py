from datetime import date

from pydantic import BaseModel, ConfigDict


class MealSlotCreate(BaseModel):
    """
    Datos necesarios para crear un hueco de comida.
    """

    meal_plan_id: int
    date: date
    meal_type: str


class MealSlotUpdate(BaseModel):
    """
    Datos permitidos para actualizar un hueco de comida.
    """

    date: date
    meal_type: str


class MealSlotResponse(BaseModel):
    """
    Datos de un hueco de comida devueltos por la API.
    """

    id: int
    meal_plan_id: int
    date: date
    meal_type: str

    model_config = ConfigDict(from_attributes=True)
