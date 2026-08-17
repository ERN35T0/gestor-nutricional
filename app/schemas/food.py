from enum import Enum

from pydantic import BaseModel, model_validator


class InventoryItemStatus(str, Enum):
    CLOSED = "closed"
    STARTED = "started"
    FROZEN = "frozen"
    CONSUMED = "consumed"


class InventoryItemCreate(BaseModel):
    """Datos necesarios para crear un elemento de inventario."""

    space_id: int
    product_id: int
    quantity: float | None = None
    unit: str | None = None
    status: InventoryItemStatus

    @model_validator(mode="after")
    def validate_quantity_and_unit(self):
        if self.quantity is not None and self.unit is None:
            raise ValueError("unit is required when quantity is provided")
        return self
