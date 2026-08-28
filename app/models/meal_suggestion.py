from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MealSuggestion(Base):
    """
    Representa una sugerencia de comida para un hueco de planificación.
    """

    __tablename__ = "meal_suggestions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    meal_slot_id: Mapped[int] = mapped_column(
        ForeignKey("meal_slots.id"),
        nullable=False,
    )

    prepared_meal_id: Mapped[int] = mapped_column(
        ForeignKey("prepared_meals.id"),
        nullable=False,
    )

    meal_slot: Mapped["MealSlot"] = relationship(
        "MealSlot",
        back_populates="suggestions",
    )

    prepared_meal: Mapped["PreparedMeal"] = relationship(
        "PreparedMeal",
        back_populates="meal_suggestions",
    )
