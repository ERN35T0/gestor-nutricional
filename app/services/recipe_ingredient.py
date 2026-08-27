from sqlalchemy.orm import Session

from app.models.recipe_ingredient import RecipeIngredient
from app.schemas.recipe_ingredient import (
    RecipeIngredientCreate,
    RecipeIngredientUpdate,
)


def create_recipe_ingredient(
    db: Session,
    ingredient: RecipeIngredientCreate,
):
    """
    Crea un ingrediente asociado a una receta.
    """

    db_ingredient = RecipeIngredient(
        recipe_id=ingredient.recipe_id,
        product_id=ingredient.product_id,
        quantity=ingredient.quantity,
        unit=ingredient.unit,
    )

    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)

    return db_ingredient


def get_recipe_ingredients(
    db: Session,
    recipe_id: int,
):
    """
    Devuelve todos los ingredientes de una receta.
    """

    return (
        db.query(RecipeIngredient)
        .filter(RecipeIngredient.recipe_id == recipe_id)
        .all()
    )


def get_recipe_ingredient(
    db: Session,
    ingredient_id: int,
):
    """
    Obtiene un ingrediente de receta por su id.
    """

    return (
        db.query(RecipeIngredient)
        .filter(RecipeIngredient.id == ingredient_id)
        .first()
    )


def update_recipe_ingredient(
    db: Session,
    ingredient_id: int,
    ingredient: RecipeIngredientUpdate,
):
    """
    Actualiza un ingrediente de receta.
    """

    db_ingredient = (
        db.query(RecipeIngredient)
        .filter(RecipeIngredient.id == ingredient_id)
        .first()
    )

    if db_ingredient is None:
        return None

    db_ingredient.quantity = ingredient.quantity
    db_ingredient.unit = ingredient.unit

    db.commit()
    db.refresh(db_ingredient)

    return db_ingredient


def delete_recipe_ingredient(
    db: Session,
    ingredient_id: int,
):
    """
    Elimina un ingrediente de receta.
    """

    db_ingredient = (
        db.query(RecipeIngredient)
        .filter(RecipeIngredient.id == ingredient_id)
        .first()
    )

    if db_ingredient is None:
        return None

    db.delete(db_ingredient)
    db.commit()

    return db_ingredient
