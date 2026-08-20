from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.schemas.food import InventoryItemCreate, InventoryItemUpdate
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.space import SpaceCreate, SpaceUpdate

from app.services.inventory import (
    create_inventory_item,
    get_inventory_items,
    get_inventory_item,
    update_inventory_item,
    delete_inventory_item,
)
from app.services.product import (
    create_product,
    get_products,
    get_product,
    update_product,
)
from app.services.space import (
    create_space,
    get_spaces,
    get_space,
    update_space,
)

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
def create_inventory_item_endpoint(
    item: InventoryItemCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un elemento de inventario.
    """

    return create_inventory_item(db, item)


@app.get("/inventory-items")
def get_inventory_items_endpoint(
    db: Session = Depends(get_db)
):
    """
    Lista todos los elementos de inventario.
    """

    return get_inventory_items(db)

@app.get("/inventory-items/{item_id}")
def get_inventory_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un elemento de inventario por id.
    """

    item = get_inventory_item(db, item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )

    return item


@app.put("/inventory-items/{item_id}")
def update_inventory_item_endpoint(
    item_id: int,
    item: InventoryItemUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un elemento de inventario.
    """

    updated_item = update_inventory_item(
        db,
        item_id,
        item
    )

    if updated_item is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )

    return updated_item


@app.delete("/inventory-items/{item_id}")
def delete_inventory_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un elemento de inventario.
    """

    item = delete_inventory_item(db, item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )

    return item


@app.post("/spaces")
def create_space_endpoint(
    space: SpaceCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo espacio."""
    return create_space(db, space)


@app.get("/spaces")
def get_spaces_endpoint(
    db: Session = Depends(get_db)
):
    """
    Lista todos los espacios.
    """

    return get_spaces(db)


@app.get("/spaces/{space_id}")
def get_space_endpoint(
    space_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un espacio por id.
    """

    space = get_space(db, space_id)

    if space is None:
        raise HTTPException(
            status_code=404,
            detail="Space not found"
        )

    return space



@app.put("/spaces/{space_id}")
def update_space_endpoint(
    space_id: int,
    space: SpaceUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un espacio.
    """

    updated_space = update_space(
        db,
        space_id,
        space
    )

    if updated_space is None:
        raise HTTPException(
            status_code=404,
            detail="Space not found"
        )

    return updated_space


@app.post("/products")
def create_product_endpoint(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo producto.
    """
    return create_product(db, product)

@app.get("/products")
def get_products_endpoint(
    db: Session = Depends(get_db)
):
    """
    Lista todos los productos.
    """

    return get_products(db)

@app.get("/products/{product_id}")
def get_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un producto por id.
    """

    product = get_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@app.put("/products/{product_id}")
def update_product_endpoint(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un producto.
    """

    updated_product = update_product(db, product_id, product)

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return updated_product
