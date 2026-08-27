from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.schemas.food import InventoryItemCreate, InventoryItemUpdate
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.space import SpaceCreate, SpaceUpdate
from app.schemas.recipe import RecipeCreate, RecipeUpdate

from app.schemas.recipe_ingredient import (
    RecipeIngredientCreate,
    RecipeIngredientUpdate,
)

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
from app.services.recipe import (
    create_recipe,
    get_recipes,
    get_recipe,
    update_recipe,
)

from app.services.recipe_ingredient import (
    create_recipe_ingredient,
    get_recipe_ingredients,
    get_recipe_ingredient,
    update_recipe_ingredient,
    delete_recipe_ingredient,
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

@app.post("/recipes")
def create_recipe_endpoint(
    recipe: RecipeCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva receta.
    """
    return create_recipe(db, recipe)


@app.get("/recipes")
def get_recipes_endpoint(
    db: Session = Depends(get_db)
):
    """
    Lista todas las recetas.
    """
    return get_recipes(db)


@app.get("/recipes/{recipe_id}")
def get_recipe_endpoint(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene una receta por id.
    """

    recipe = get_recipe(db, recipe_id)

    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    return recipe


@app.put("/recipes/{recipe_id}")
def update_recipe_endpoint(
    recipe_id: int,
    recipe: RecipeUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza una receta.
    """

    updated_recipe = update_recipe(
        db,
        recipe_id,
        recipe
    )

    if updated_recipe is None:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    return updated_recipe

@app.post("/recipe-ingredients")
def create_recipe_ingredient_endpoint(
    ingredient: RecipeIngredientCreate,
    db: Session = Depends(get_db),
):
    """
    Añade un ingrediente a una receta.
    """

    return create_recipe_ingredient(db, ingredient)

@app.get("/recipes/{recipe_id}/ingredients")
def get_recipe_ingredients_endpoint(
    recipe_id: int,
    db: Session = Depends(get_db),
):
    """
    Lista todos los ingredientes de una receta.
    """

    return get_recipe_ingredients(db, recipe_id)

@app.get("/recipe-ingredients/{ingredient_id}")
def get_recipe_ingredient_endpoint(
    ingredient_id: int,
    db: Session = Depends(get_db),
):
    """
    Obtiene un ingrediente de receta por id.
    """

    ingredient = get_recipe_ingredient(db, ingredient_id)

    if ingredient is None:
        raise HTTPException(
            status_code=404,
            detail="Recipe ingredient not found",
        )

    return ingredient

@app.put("/recipe-ingredients/{ingredient_id}")
def update_recipe_ingredient_endpoint(
    ingredient_id: int,
    ingredient: RecipeIngredientUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualiza un ingrediente de receta.
    """

    updated_ingredient = update_recipe_ingredient(
        db,
        ingredient_id,
        ingredient,
    )

    if updated_ingredient is None:
        raise HTTPException(
            status_code=404,
            detail="Recipe ingredient not found",
        )

    return updated_ingredient

@app.delete("/recipe-ingredients/{ingredient_id}")
def delete_recipe_ingredient_endpoint(
    ingredient_id: int,
    db: Session = Depends(get_db),
):
    """
    Elimina un ingrediente de receta.
    """

    ingredient = delete_recipe_ingredient(db, ingredient_id)

    if ingredient is None:
        raise HTTPException(
            status_code=404,
            detail="Recipe ingredient not found",
        )

    return ingredient

