from sqlalchemy.orm import Session

from app.models.meal_plan import MealPlan
from app.schemas.meal_plan import MealPlanCreate, MealPlanUpdate
from app.exceptions import MealPlanConfirmedError

def create_meal_plan(
    db: Session,
    plan: MealPlanCreate,
):
    """
    Crea una planificación.
    """

    db_plan = MealPlan(
        start_date=plan.start_date,
        end_date=plan.end_date,
    )

    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)

    return db_plan


def get_meal_plans(db: Session):
    """
    Devuelve todas las planificaciones.
    """

    return db.query(MealPlan).all()


def get_meal_plan(
    db: Session,
    plan_id: int,
):
    """
    Obtiene una planificación por su id.
    """

    return (
        db.query(MealPlan)
        .filter(MealPlan.id == plan_id)
        .first()
    )


def update_meal_plan(
    db: Session,
    plan_id: int,
    plan: MealPlanUpdate,
):
    """
    Actualiza una planificación.
    """

    db_plan = (
        db.query(MealPlan)
        .filter(MealPlan.id == plan_id)
        .first()
    )

    if db_plan is None:
        return None

    if db_plan.status == "confirmed":
        raise MealPlanConfirmedError

    db_plan.start_date = plan.start_date
    db_plan.end_date = plan.end_date

    db.commit()
    db.refresh(db_plan)

    return db_plan


def delete_meal_plan(
    db: Session,
    plan_id: int,
):
    """
    Elimina una planificación.
    """

    db_plan = (
        db.query(MealPlan)
        .filter(MealPlan.id == plan_id)
        .first()
    )

    if db_plan is None:
        return None

    db.delete(db_plan)
    db.commit()

    return db_plan

def confirm_meal_plan(
    db: Session,
    plan_id: int,
):
    """
    Confirma una planificación si todos sus slots tienen
    exactamente una sugerencia seleccionada.
    """
    db_plan = (
        db.query(MealPlan)
        .filter(MealPlan.id == plan_id)
        .first()
    )

    if db_plan is None:
        return None

    if not db_plan.meal_slots:
        raise ValueError("Meal plan must have at least one meal slot")

    for slot in db_plan.meal_slots:
        selected_suggestions = [
            suggestion
            for suggestion in slot.suggestions
            if suggestion.status == "selected"
        ]

        if len(selected_suggestions) != 1:
            raise ValueError(
                "Every meal slot must have exactly one selected suggestion"
            )

    db_plan.status = "confirmed"

    db.commit()
    db.refresh(db_plan)

    return db_plan
