from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class RecipeIngredient(Base):
    """
    Representa un ingrediente utilizado por una receta.
    """

    __tablename__ = "recipe_ingredients"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
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

    # Cada ingrediente pertenece a una única receta.
    recipe: Mapped["Recipe"] = relationship(
        "Recipe",
        back_populates="ingredients",
    )

    # Cada ingrediente utiliza un único producto del catálogo.
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="recipe_ingredients",
    )
