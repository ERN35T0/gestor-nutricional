from sqlalchemy.orm import Session

from app.models.prepared_meal import PreparedMeal
from app.schemas.prepared_meal import (
    PreparedMealCreate,
    PreparedMealUpdate,
)


def create_prepared_meal(
    db: Session,
    meal: PreparedMealCreate,
):
    """
    Crea una preparación o comida preparada.
    """

    db_meal = PreparedMeal(
        name=meal.name,
        type=meal.type.value,
        quantity=meal.quantity,
        unit=meal.unit,
        recipe_id=meal.recipe_id,
        expires_at=meal.expires_at,
    )

    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)

    return db_meal


def get_prepared_meals(db: Session):
    """
    Devuelve todas las preparaciones y comidas preparadas.
    """

    return db.query(PreparedMeal).all()


def get_prepared_meal(
    db: Session,
    meal_id: int,
):
    """
    Obtiene una preparación o comida preparada por su id.
    """

    return (
        db.query(PreparedMeal)
        .filter(PreparedMeal.id == meal_id)
        .first()
    )


def update_prepared_meal(
    db: Session,
    meal_id: int,
    meal: PreparedMealUpdate,
):
    """
    Actualiza una preparación o comida preparada.
    """

    db_meal = (
        db.query(PreparedMeal)
        .filter(PreparedMeal.id == meal_id)
        .first()
    )

    if db_meal is None:
        return None

    db_meal.name = meal.name
    db_meal.quantity = meal.quantity
    db_meal.unit = meal.unit
    db_meal.expires_at = meal.expires_at

    db.commit()
    db.refresh(db_meal)

    return db_meal


def delete_prepared_meal(
    db: Session,
    meal_id: int,
):
    """
    Elimina una preparación o comida preparada.
    """

    db_meal = (
        db.query(PreparedMeal)
        .filter(PreparedMeal.id == meal_id)
        .first()
    )

    if db_meal is None:
        return None

    db.delete(db_meal)
    db.commit()

    return db_meal
