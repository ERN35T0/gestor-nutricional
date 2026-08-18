from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(db: Session, product: ProductCreate):
    """
    Crea un producto y lo guarda en la base de datos.
    """

    db_product = Product(
        name=product.name
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

def get_product(db: Session, product_id: int):
    """
    Obtiene un producto por su id.
    """

    return (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )


def get_products(db: Session):
    """
    Devuelve todos los productos almacenados.
    """

    return db.query(Product).all()
