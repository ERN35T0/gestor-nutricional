from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, model_validator


class PreparedMealType(str, Enum):
    PREPARATION = "preparation"
    MEAL = "meal"


class PreparedMealCreate(BaseModel):
    """
    Datos necesarios para crear una preparación o comida preparada.
    """

    name: str
    type: PreparedMealType
    quantity: float | None = None
    unit: str | None = None
    recipe_id: int | None = None
    expires_at: datetime | None = None

    @model_validator(mode="after")
    def validate_quantity_and_unit(self):
        if self.quantity is not None and self.unit is None:
            raise ValueError("unit is required when quantity is provided")
        return self


class PreparedMealUpdate(BaseModel):
    """
    Datos permitidos para actualizar una preparación o comida preparada.
    """

    name: str
    quantity: float | None = None
    unit: str | None = None
    expires_at: datetime | None = None

    @model_validator(mode="after")
    def validate_quantity_and_unit(self):
        if self.quantity is not None and self.unit is None:
            raise ValueError("unit is required when quantity is provided")
        return self


class PreparedMealResponse(BaseModel):
    """
    Datos de una preparación o comida preparada devueltos por la API.
    """

    id: int
    name: str
    type: PreparedMealType
    quantity: float | None = None
    unit: str | None = None
    recipe_id: int | None = None
    created_at: datetime
    expires_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
