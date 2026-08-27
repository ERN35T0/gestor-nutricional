from sqlalchemy.orm import Session

from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate


def create_recipe(db: Session, recipe: RecipeCreate):
    """
    Crea una receta y la guarda en la base de datos.
    """

    db_recipe = Recipe(
        name=recipe.name
    )

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe


def get_recipe(db: Session, recipe_id: int):
    """
    Obtiene una receta por su id.
    """

    return (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id)
        .first()
    )


def get_recipes(db: Session):
    """
    Devuelve todas las recetas almacenadas.
    """

    return db.query(Recipe).all()


def update_recipe(
    db: Session,
    recipe_id: int,
    recipe: RecipeUpdate
):
    """
    Actualiza una receta existente.
    """

    db_recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id)
        .first()
    )

    if db_recipe is None:
        return None

    db_recipe.name = recipe.name

    db.commit()
    db.refresh(db_recipe)

    return db_recipe
