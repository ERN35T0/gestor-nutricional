from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    """
    Datos necesarios para crear un producto.
    """

    name: str


class ProductUpdate(BaseModel):
    """
    Datos permitidos para actualizar un producto.
    """

    name: str


class ProductResponse(BaseModel):
    """
    Datos devueltos por la API.
    """

    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
