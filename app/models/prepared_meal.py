from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PreparedMeal(Base):
    """
    Representa una preparación o comida preparada.
    """

    __tablename__ = "prepared_meals"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    quantity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    unit: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    recipe_id: Mapped[int | None] = mapped_column(
        ForeignKey("recipes.id"),
        nullable=True,
    )

    # Una comida preparada puede proceder de una receta.
    recipe: Mapped["Recipe | None"] = relationship(
        "Recipe",
        back_populates="prepared_meals",
    )

    # Una comida preparada puede aparecer en varias sugerencias.
    meal_suggestions: Mapped[list["MealSuggestion"]] = relationship(
        "MealSuggestion",
        back_populates="prepared_meal",
    )
