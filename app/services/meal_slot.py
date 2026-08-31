from sqlalchemy.orm import Session

from app.models.meal_slot import MealSlot
from app.schemas.meal_slot import MealSlotCreate, MealSlotUpdate
from app.models.meal_plan import MealPlan
from app.exceptions import MealSlotDateOutOfRangeError


def create_meal_slot(
    db: Session,
    slot: MealSlotCreate,
):
    """
    Crea un hueco de comida.
    """
    meal_plan = (
        db.query(MealPlan)
        .filter(MealPlan.id == slot.meal_plan_id)
        .first()
    )

    if meal_plan is None:
        return None

    # Un hueco solo puede existir dentro del periodo
    # definido por su planificación.
    if (
        slot.date < meal_plan.start_date
        or slot.date > meal_plan.end_date
    ):
        raise MealSlotDateOutOfRangeError

    db_slot = MealSlot(
        meal_plan_id=slot.meal_plan_id,
        date=slot.date,
        meal_type=slot.meal_type,
    )

    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)

    return db_slot


def get_meal_slots(db: Session):
    """
    Devuelve todos los huecos de comida.
    """
    return db.query(MealSlot).all()


def get_meal_slot(
    db: Session,
    slot_id: int,
):
    """
    Obtiene un hueco de comida por su id.
    """
    return (
        db.query(MealSlot)
        .filter(MealSlot.id == slot_id)
        .first()
    )


def update_meal_slot(
    db: Session,
    slot_id: int,
    slot: MealSlotUpdate,
):
    """
    Actualiza un hueco de comida.
    """

    # Primero buscamos el slot que queremos modificar.
    db_slot = (
        db.query(MealSlot)
        .filter(MealSlot.id == slot_id)
        .first()
    )

    if db_slot is None:
        return None

    # Recuperamos la planificación a la que pertenece el slot.
    meal_plan = (
        db.query(MealPlan)
        .filter(MealPlan.id == db_slot.meal_plan_id)
        .first()
    )

    # Comprobamos que la nueva fecha siga dentro de la planificación.
    if (
        slot.date < meal_plan.start_date
        or slot.date > meal_plan.end_date
    ):
        raise MealSlotDateOutOfRangeError

    # Si la fecha es válida, actualizamos los datos.
    db_slot.date = slot.date
    db_slot.meal_type = slot.meal_type

    db.commit()
    db.refresh(db_slot)

    return db_slot


def delete_meal_slot(
    db: Session,
    slot_id: int,
):
    """
    Elimina un hueco de comida.
    """
    db_slot = (
        db.query(MealSlot)
        .filter(MealSlot.id == slot_id)
        .first()
    )

    if db_slot is None:
        return None

    db.delete(db_slot)
    db.commit()

    return db_slot
