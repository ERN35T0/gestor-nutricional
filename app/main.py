from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.schemas.food import InventoryItemCreate
from app.services.inventory import create_inventory_item
from app.schemas.space import SpaceCreate
from app.services.space import create_space
from app.schemas.product import ProductCreate
from app.services.product import create_product

app = FastAPI()

def get_db():
    """
    Proporciona una sesión de base de datos por petición.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Gestor Nutricional funcionando"}


@app.post("/inventory-items")
def create_inventory_item_endpoint(item: InventoryItemCreate):
    return create_inventory_item(item)


@app.post("/spaces")
def create_space_endpoint(space: SpaceCreate):
    """Crea un nuevo espacio."""
    return create_space(space)

@app.post("/products")
def create_product_endpoint(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo producto.
    """
    return create_product(db, product)
