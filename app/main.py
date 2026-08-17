from fastapi import FastAPI

from app.schemas.food import InventoryItemCreate
from app.services.inventory import create_inventory_item

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Gestor Nutricional funcionando"}


@app.post("/foods")
def create_inventory_item_endpoint(item: InventoryItemCreate):
    return create_inventory_item(item)
