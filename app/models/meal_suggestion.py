from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MealSuggestion(Base):
    """
    Representa una sugerencia de comida para un hueco de planificación.
    """

    __tablename__ = "meal_suggestions"

    # Una misma comida no puede aparecer dos veces como sugerencia
    # dentro del mismo hueco de planificación.
    __table_args__ = (
        UniqueConstraint(
            "meal_slot_id",
            "prepared_meal_id",
            name="uq_meal_suggestion_slot_meal",
        ),
    )

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

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False,
    )

    generation: Mapped[int] = mapped_column(
        Integer,
        default=1,
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
