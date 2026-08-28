from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Recipe(Base):
    """
    Modelo SQLAlchemy para recetas.
    """

    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Una receta puede tener muchos ingredientes.
    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )

    # Una receta puede dar lugar a varias preparaciones/comidas.
    prepared_meals: Mapped[list["PreparedMeal"]] = relationship(
        "PreparedMeal",
        back_populates="recipe",
    )
