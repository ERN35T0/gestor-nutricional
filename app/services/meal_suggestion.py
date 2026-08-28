from sqlalchemy.orm import Session

from app.models.meal_slot import MealSlot
from app.models.meal_suggestion import MealSuggestion
from app.models.prepared_meal import PreparedMeal
from app.schemas.meal_suggestion import MealSuggestionCreate


def create_meal_suggestion(
    db: Session,
    suggestion: MealSuggestionCreate,
):
    """
    Crea una sugerencia de comida.
    """

    meal_slot = (
        db.query(MealSlot)
        .filter(MealSlot.id == suggestion.meal_slot_id)
        .first()
    )

    if meal_slot is None:
        return None

    prepared_meal = (
        db.query(PreparedMeal)
        .filter(PreparedMeal.id == suggestion.prepared_meal_id)
        .first()
    )

    if prepared_meal is None:
        return None

    db_suggestion = MealSuggestion(
        meal_slot_id=suggestion.meal_slot_id,
        prepared_meal_id=suggestion.prepared_meal_id,
    )

    db.add(db_suggestion)
    db.commit()
    db.refresh(db_suggestion)

    return db_suggestion


def get_meal_suggestions(db: Session):
    """
    Devuelve todas las sugerencias de comida.
    """

    return db.query(MealSuggestion).all()


def get_meal_suggestion(
    db: Session,
    suggestion_id: int,
):
    """
    Obtiene una sugerencia por su id.
    """

    return (
        db.query(MealSuggestion)
        .filter(MealSuggestion.id == suggestion_id)
        .first()
    )


def get_meal_suggestions_for_slot(
    db: Session,
    meal_slot_id: int,
):
    """
    Devuelve las sugerencias de comida de un hueco concreto.
    """
    return (
        db.query(MealSuggestion)
        .filter(MealSuggestion.meal_slot_id == meal_slot_id)
        .all()
    )

def delete_meal_suggestion(
    db: Session,
    suggestion_id: int,
):
    """
    Elimina una sugerencia de comida.
    """

    db_suggestion = (
        db.query(MealSuggestion)
        .filter(MealSuggestion.id == suggestion_id)
        .first()
    )

    if db_suggestion is None:
        return None

    db.delete(db_suggestion)
    db.commit()

    return db_suggestion
