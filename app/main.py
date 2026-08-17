from fastapi import FastAPI

from app.schemas.food import InventoryItemCreate
from app.services.inventory import create_inventory_item
from app.schemas.space import SpaceCreate
from app.services.space import create_space

app = FastAPI()


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
