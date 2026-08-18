from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(product: ProductCreate) -> Product:
    """Crea un Product a partir de los datos validados de entrada."""
    return Product(name=product.name)
