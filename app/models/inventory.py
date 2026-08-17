from dataclasses import dataclass
from datetime import datetime

from app.schemas.food import InventoryItemStatus


@dataclass
class InventoryItem:
    """Representa una existencia concreta de un producto en un espacio."""

    space_id: int
    product_id: int
    status: InventoryItemStatus
    quantity: float | None = None
    unit: str | None = None
    created_at: datetime | None = None
    status_changed_at: datetime | None = None
