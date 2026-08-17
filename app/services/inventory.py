from datetime import datetime

from app.models.inventory import InventoryItem
from app.schemas.food import InventoryItemCreate


def create_inventory_item(item: InventoryItemCreate) -> InventoryItem:
    """Crea un InventoryItem a partir de los datos validados de entrada."""
    now = datetime.now()

    return InventoryItem(
        space_id=item.space_id,
        product_id=item.product_id,
        status=item.status,
        quantity=item.quantity,
        unit=item.unit,
        created_at=now,
        status_changed_at=now,
    )
