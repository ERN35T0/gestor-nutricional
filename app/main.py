from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.exceptions import MealSlotDateOutOfRangeError

from app.schemas.food import InventoryItemCreate, InventoryItemUpdate
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.space import SpaceCreate, SpaceUpdate
from app.schemas.recipe import RecipeCreate, RecipeUpdate
from app.schemas.meal_plan import MealPlanCreate, MealPlanUpdate
from app.schemas.meal_suggestion import MealSuggestionCreate

from app.schemas.recipe_ingredient import (
    RecipeIngredientCreate,
    RecipeIngredientUpdate,
)

from app.schemas.prepared_meal import (
    PreparedMealCreate,
    PreparedMealUpdate,
)

from app.schemas.meal_slot import (
    MealSlotCreate,
    MealSlotUpdate,
    MealSlotResponse,  # Respuesta que devuelve la API.
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

from app.services.prepared_meal import (
    create_prepared_meal,
    get_prepared_meals,
    get_prepared_meal,
    update_prepared_meal,
    delete_prepared_meal,
)

from app.services.meal_plan import (
    create_meal_plan,
    get_meal_plans,
    get_meal_plan,
    update_meal_plan,
    delete_meal_plan,
)

from app.services.meal_slot import (
    create_meal_slot,
    get_meal_slots,
    get_meal_slot,
    update_meal_slot,
    delete_meal_slot,
)

from app.services.meal_suggestion import (
    create_meal_suggestion,
    get_meal_suggestions,
    get_meal_suggestions_for_slot,
    get_meal_suggestion,
    delete_meal_suggestion,
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

@app.post("/prepared-meals")
def create_prepared_meal_endpoint(
    meal: PreparedMealCreate,
    db: Session = Depends(get_db),
):
    """
    Crea una preparación o comida preparada.
    """

    return create_prepared_meal(db, meal)


@app.get("/prepared-meals")
def get_prepared_meals_endpoint(
    db: Session = Depends(get_db),
):
    """
    Lista todas las preparaciones y comidas preparadas.
    """

    return get_prepared_meals(db)


@app.get("/prepared-meals/{meal_id}")
def get_prepared_meal_endpoint(
    meal_id: int,
    db: Session = Depends(get_db),
):
    """
    Obtiene una preparación o comida preparada por id.
    """

    meal = get_prepared_meal(db, meal_id)

    if meal is None:
        raise HTTPException(
            status_code=404,
            detail="Prepared meal not found",
        )

    return meal


@app.put("/prepared-meals/{meal_id}")
def update_prepared_meal_endpoint(
    meal_id: int,
    meal: PreparedMealUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualiza una preparación o comida preparada.
    """

    updated_meal = update_prepared_meal(
        db,
        meal_id,
        meal,
    )

    if updated_meal is None:
        raise HTTPException(
            status_code=404,
            detail="Prepared meal not found",
        )

    return updated_meal


@app.delete("/prepared-meals/{meal_id}")
def delete_prepared_meal_endpoint(
    meal_id: int,
    db: Session = Depends(get_db),
):
    """
    Elimina una preparación o comida preparada.
    """

    meal = delete_prepared_meal(db, meal_id)

    if meal is None:
        raise HTTPException(
            status_code=404,
            detail="Prepared meal not found",
        )

    return meal

@app.post("/meal-plans")
def create_meal_plan_endpoint(
    plan: MealPlanCreate,
    db: Session = Depends(get_db),
):
    """
    Crea una planificación.
    """
    return create_meal_plan(db, plan)


@app.get("/meal-plans")
def get_meal_plans_endpoint(
    db: Session = Depends(get_db),
):
    """
    Lista todas las planificaciones.
    """
    return get_meal_plans(db)


@app.get("/meal-plans/{plan_id}")
def get_meal_plan_endpoint(
    plan_id: int,
    db: Session = Depends(get_db),
):
    """
    Obtiene una planificación por id.
    """
    plan = get_meal_plan(db, plan_id)

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Meal plan not found",
        )

    return plan


@app.put("/meal-plans/{plan_id}")
def update_meal_plan_endpoint(
    plan_id: int,
    plan: MealPlanUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualiza una planificación.
    """
    updated_plan = update_meal_plan(
        db,
        plan_id,
        plan,
    )

    if updated_plan is None:
        raise HTTPException(
            status_code=404,
            detail="Meal plan not found",
        )

    return updated_plan


@app.delete("/meal-plans/{plan_id}")
def delete_meal_plan_endpoint(
    plan_id: int,
    db: Session = Depends(get_db),
):
    """
    Elimina una planificación.
    """
    plan = delete_meal_plan(db, plan_id)

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Meal plan not found",
        )

    return plan

@app.post("/meal-slots")
def create_meal_slot_endpoint(
    slot: MealSlotCreate,
    db: Session = Depends(get_db),
):
    """
    Crea un hueco de comida.
    """
    try:
        created_slot = create_meal_slot(db, slot)

    except MealSlotDateOutOfRangeError:
        # El MealPlan existe, pero la fecha no pertenece a su periodo.
        raise HTTPException(
            status_code=400,
            detail="Meal slot date is outside meal plan range",
        )

    if created_slot is None:
        # El MealPlan indicado no existe.
        raise HTTPException(
            status_code=404,
            detail="Meal plan not found",
        )

    return created_slot


@app.get("/meal-slots")
def get_meal_slots_endpoint(
    db: Session = Depends(get_db),
):
    """
    Lista todos los huecos de comida.
    """
    return get_meal_slots(db)


@app.get("/meal-slots/{slot_id}")
def get_meal_slot_endpoint(
    slot_id: int,
    db: Session = Depends(get_db),
):
    """
    Obtiene un hueco de comida por id.
    """
    slot = get_meal_slot(db, slot_id)

    if slot is None:
        raise HTTPException(
            status_code=404,
            detail="Meal slot not found",
        )

    return slot


@app.put("/meal-slots/{slot_id}", response_model=MealSlotResponse)
def update_meal_slot_endpoint(
    slot_id: int,
    slot: MealSlotUpdate,
    db: Session = Depends(get_db),
):
    try:
        # El servicio se encarga de validar la regla de negocio.
        updated_slot = update_meal_slot(
            db,
            slot_id,
            slot,
        )

    except MealSlotDateOutOfRangeError:
        # Convertimos la excepción de dominio en una respuesta HTTP 400.
        raise HTTPException(
            status_code=400,
            detail="Meal slot date must be within meal plan date range",
        )

    if updated_slot is None:
        # Si el slot no existe, mantenemos el 404.
        raise HTTPException(
            status_code=404,
            detail="Meal slot not found",
        )

    return updated_slot


@app.delete("/meal-slots/{slot_id}")
def delete_meal_slot_endpoint(
    slot_id: int,
    db: Session = Depends(get_db),
):
    """
    Elimina un hueco de comida.
    """
    slot = delete_meal_slot(db, slot_id)

    if slot is None:
        raise HTTPException(
            status_code=404,
        detail="Meal slot not found",
    )

    return slot


@app.post("/meal-suggestions")
def create_meal_suggestion_endpoint(
    suggestion: MealSuggestionCreate,
    db: Session = Depends(get_db),
):
    """
    Crea una sugerencia de comida.
    """
    created_suggestion = create_meal_suggestion(
        db,
        suggestion,
    )

    if created_suggestion is None:
        raise HTTPException(
            status_code=404,
            detail="Meal slot or prepared meal not found",
        )

    return created_suggestion


@app.get("/meal-suggestions")
def get_meal_suggestions_endpoint(
    db: Session = Depends(get_db),
):
    """
    Lista todas las sugerencias de comida.
    """
    return get_meal_suggestions(db)


@app.get("/meal-slots/{meal_slot_id}/suggestions")
def get_meal_suggestions_for_slot_endpoint(
    meal_slot_id: int,
    db: Session = Depends(get_db),
):
    """
    Lista las sugerencias de comida de un hueco concreto.
    """
    return get_meal_suggestions_for_slot(
        db,
        meal_slot_id,
    )


@app.get("/meal-suggestions/{suggestion_id}")
def get_meal_suggestion_endpoint(
    suggestion_id: int,
    db: Session = Depends(get_db),
):
    """
    Obtiene una sugerencia de comida por id.
    """
    suggestion = get_meal_suggestion(
        db,
        suggestion_id,
    )

    if suggestion is None:
        raise HTTPException(
            status_code=404,
            detail="Meal suggestion not found",
        )

    return suggestion


@app.delete("/meal-suggestions/{suggestion_id}")
def delete_meal_suggestion_endpoint(
    suggestion_id: int,
    db: Session = Depends(get_db),
):
    """
    Elimina una sugerencia de comida.
    """
    suggestion = delete_meal_suggestion(
        db,
        suggestion_id,
    )

    if suggestion is None:
        raise HTTPException(
            status_code=404,
            detail="Meal suggestion not found",
        )

    return suggestion
