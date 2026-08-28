from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MealSlot(Base):
    """
    Representa una ocasión concreta dentro de una planificación.
    """

    __tablename__ = "meal_slots"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    meal_plan_id: Mapped[int] = mapped_column(
        ForeignKey("meal_plans.id"),
        nullable=False,
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    meal_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    meal_plan: Mapped["MealPlan"] = relationship(
        "MealPlan",
        back_populates="meal_slots",
    )

    suggestions: Mapped[list["MealSuggestion"]] = relationship(
        "MealSuggestion",
        back_populates="meal_slot",
        cascade="all, delete-orphan",
    )
