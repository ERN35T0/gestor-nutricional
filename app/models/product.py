from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Product(Base):
    """
    Modelo SQLAlchemy para productos del catálogo de alimentos.
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Un producto puede aparecer como ingrediente en varias recetas.
    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        "RecipeIngredient",
        back_populates="product",
    )

    # Un producto puede tener varias existencias en el inventario.
    inventory_items: Mapped[list["InventoryItem"]] = relationship(
        "InventoryItem",
        back_populates="product",
    )
