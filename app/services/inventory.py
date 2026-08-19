from datetime import datetime

from sqlalchemy.orm import Session

from app.models.inventory import InventoryItem
from app.schemas.food import InventoryItemCreate, InventoryItemUpdate


def create_inventory_item(
    db: Session,
    item: InventoryItemCreate
):
    """
    Crea un elemento de inventario y lo guarda en la base de datos.
    """

    db_item = InventoryItem(
        space_id=item.space_id,
        product_id=item.product_id,
        status=item.status,
        quantity=item.quantity,
        unit=item.unit,
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def get_inventory_items(db: Session):
    """
    Devuelve todos los elementos de inventario almacenados.
    """

    return db.query(InventoryItem).all()


def get_inventory_item(db: Session, item_id: int):
    """
    Obtiene un elemento de inventario por su id.
    """

    return (
        db.query(InventoryItem)
        .filter(InventoryItem.id == item_id)
        .first()
    )


def update_inventory_item(
    db: Session,
    item_id: int,
    item: InventoryItemUpdate
):
    """
    Actualiza un elemento de inventario.
    """

    db_item = (
        db.query(InventoryItem)
        .filter(InventoryItem.id == item_id)
        .first()
    )

    if db_item is None:
        return None

    status_changed = db_item.status != item.status

    db_item.quantity = item.quantity
    db_item.unit = item.unit
    db_item.status = item.status

    if status_changed:
        db_item.status_changed_at = datetime.utcnow()

    db.commit()
    db.refresh(db_item)

    return db_item

def delete_inventory_item(db: Session, item_id: int):
    """
    Elimina un elemento de inventario.
    """

    db_item = (
        db.query(InventoryItem)
        .filter(InventoryItem.id == item_id)
        .first()
    )

    if db_item is None:
        return None

    db.delete(db_item)
    db.commit()

    return db_item
