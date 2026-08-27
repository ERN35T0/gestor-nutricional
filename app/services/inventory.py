from datetime import UTC, datetime

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
    # Validar transición de estados
    allowed_transitions = {
        "available": ["started", "consumed"],
        "started": ["consumed"],
        "consumed": []  # No se permite cambiar una vez consumido
    }

    new_status = item.status.value if hasattr(item.status, 'value') else item.status
    current_status = db_item.status

    if new_status != current_status:
        if new_status not in allowed_transitions.get(current_status, []):
            # La transición no está permitida → lanzamos error
            raise ValueError(
                f"Transición de estado inválida: {current_status} → {new_status}"
            )
        db_item.status = new_status
        db_item.status_changed_at = datetime.now(UTC)
    else:
        if status_changed:
            db_item.status_changed_at = datetime.now(UTC)

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
