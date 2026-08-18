from pydantic import BaseModel


class ProductCreate(BaseModel):
    """Datos necesarios para crear un producto."""

    name: str
