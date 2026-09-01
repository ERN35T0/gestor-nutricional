from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import MealSuggestionAlreadyExistsError
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
        status="pending",
    )

    db.add(db_suggestion)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise MealSuggestionAlreadyExistsError

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


def update_meal_suggestion_status(
    db: Session,
    suggestion_id: int,
    status: str,
):
    """
    Actualiza el estado de una sugerencia de comida.
    """
    db_suggestion = (
        db.query(MealSuggestion)
        .filter(MealSuggestion.id == suggestion_id)
        .first()
    )

    if db_suggestion is None:
        return None

    if status == "selected":
        selected_suggestion = (
            db.query(MealSuggestion)
            .filter(
                MealSuggestion.meal_slot_id
                == db_suggestion.meal_slot_id,
                MealSuggestion.status == "selected",
                MealSuggestion.id != suggestion_id,
            )
            .first()
        )

        if selected_suggestion is not None:
            return "already_selected"

    db_suggestion.status = status

    db.commit()
    db.refresh(db_suggestion)

    return db_suggestion


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

def generate_meal_suggestions(
    db: Session,
    meal_slot_id: int,
):
    """
    Genera hasta dos sugerencias de comida para un hueco.
    """
    meal_slot = (
        db.query(MealSlot)
        .filter(MealSlot.id == meal_slot_id)
        .first()
    )

    if meal_slot is None:
        return None

    generation = get_next_meal_suggestion_generation(
        db,
        meal_slot_id,
    )

    if generation is None:
        return "generation_not_available"

    suggested_meal_ids = (
        db.query(MealSuggestion.prepared_meal_id)
        .filter(MealSuggestion.meal_slot_id == meal_slot_id)
        .all()
    )

    suggested_meal_ids = [
        meal_id
        for (meal_id,) in suggested_meal_ids
    ]

    available_meals = (
        db.query(PreparedMeal)
        .filter(~PreparedMeal.id.in_(suggested_meal_ids))
        .order_by(PreparedMeal.created_at.asc())
        .limit(2)
        .all()
    )

    suggestions = []

    for prepared_meal in available_meals:
        db_suggestion = MealSuggestion(
            meal_slot_id=meal_slot_id,
            prepared_meal_id=prepared_meal.id,
            status="pending",
            generation=generation,
        )

        db.add(db_suggestion)
        suggestions.append(db_suggestion)

    db.commit()

    for suggestion in suggestions:
        db.refresh(suggestion)

    return suggestions

def get_next_meal_suggestion_generation(
    db: Session,
    meal_slot_id: int,
):
    """
    Determina si un hueco puede recibir una nueva generación
    de sugerencias.
    """
    suggestions = (
        db.query(MealSuggestion)
        .filter(MealSuggestion.meal_slot_id == meal_slot_id)
        .all()
    )

    if not suggestions:
        return 1

    generation_one = [
        suggestion
        for suggestion in suggestions
        if suggestion.generation == 1
    ]

    generation_two = [
        suggestion
        for suggestion in suggestions
        if suggestion.generation == 2
    ]

    if (
        len(generation_one) == 2
        and all(
            suggestion.status == "rejected"
            for suggestion in generation_one
        )
        and not generation_two
    ):
        return 2

    return None
