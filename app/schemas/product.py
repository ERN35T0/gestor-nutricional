from pydantic import BaseModel


class ProductCreate(BaseModel):
    """
    Datos necesarios para crear un producto.
    """

    name: str


class ProductResponse(BaseModel):
    """
    Datos devueltos por la API.
    """

    id: int
    name: str

    class Config:
        from_attributes = True
