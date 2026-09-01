from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, model_validator


class MealPlanCreate(BaseModel):
    """
    Datos necesarios para crear una planificación.
    """

    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self


class MealPlanUpdate(BaseModel):
    """
    Datos permitidos para actualizar una planificación.
    """

    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self


class MealPlanResponse(BaseModel):
    """
    Datos de una planificación devueltos por la API.
    """

    id: int
    start_date: date
    end_date: date
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
