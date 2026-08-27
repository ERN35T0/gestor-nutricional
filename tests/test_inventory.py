def test_create_inventory_item(
    client,
    create_space,
    create_product
):
    response = client.post(
        "/inventory-items",
        json={
            "space_id": create_space["id"],
            "product_id": create_product["id"],
            "quantity": 2,
            "unit": "kg",
            "status": "available"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["space_id"] == create_space["id"]
    assert data["product_id"] == create_product["id"]
    assert data["quantity"] == 2
    assert data["unit"] == "kg"
    assert data["status"] == "available"


def test_get_inventory_items(
    client,
    create_space,
    create_product
):
    client.post(
        "/inventory-items",
        json={
            "space_id": create_space["id"],
            "product_id": create_product["id"],
            "quantity": 2,
            "unit": "kg",
            "status": "available"
        }
    )

    response = client.get("/inventory-items")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["space_id"] == create_space["id"]
    assert data[0]["product_id"] == create_product["id"]
    assert data[0]["quantity"] == 2
    assert data[0]["unit"] == "kg"
    assert data[0]["status"] == "available"


def test_get_inventory_item(
    client,
    create_space,
    create_product
):
    create_response = client.post(
        "/inventory-items",
        json={
            "space_id": create_space["id"],
            "product_id": create_product["id"],
            "quantity": 2,
            "unit": "kg",
            "status": "available"
        }
    )

    item_id = create_response.json()["id"]

    response = client.get(
        f"/inventory-items/{item_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id
    assert data["space_id"] == create_space["id"]
    assert data["product_id"] == create_product["id"]
    assert data["quantity"] == 2
    assert data["unit"] == "kg"
    assert data["status"] == "available"


def test_update_inventory_item(
    client,
    create_space,
    create_product
):
    create_response = client.post(
        "/inventory-items",
        json={
            "space_id": create_space["id"],
            "product_id": create_product["id"],
            "quantity": 2,
            "unit": "kg",
            "status": "available"
        }
    )

    item = create_response.json()

    item_id = item["id"]
    original_status_changed_at = item["status_changed_at"]

    response = client.put(
        f"/inventory-items/{item_id}",
        json={
            "quantity": 1,
            "unit": "kg",
            "status": "started"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id
    assert data["quantity"] == 1
    assert data["unit"] == "kg"
    assert data["status"] == "started"

    assert (
        data["status_changed_at"]
        != original_status_changed_at
    )


def test_update_inventory_item_without_status_change(
    client,
    create_space,
    create_product
):
    create_response = client.post(
        "/inventory-items",
        json={
            "space_id": create_space["id"],
            "product_id": create_product["id"],
            "quantity": 2,
            "unit": "kg",
            "status": "started"
        }
    )

    item = create_response.json()

    item_id = item["id"]
    original_status_changed_at = item["status_changed_at"]

    response = client.put(
        f"/inventory-items/{item_id}",
        json={
            "quantity": 3,
            "unit": "kg",
            "status": "started"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["quantity"] == 3
    assert data["unit"] == "kg"
    assert data["status"] == "started"

    assert (
        data["status_changed_at"]
        == original_status_changed_at
    )


def test_delete_inventory_item(
    client,
    create_space,
    create_product
):
    create_response = client.post(
        "/inventory-items",
        json={
            "space_id": create_space["id"],
            "product_id": create_product["id"],
            "quantity": 2,
            "unit": "kg",
            "status": "available"
        }
    )

    item_id = create_response.json()["id"]

    response = client.delete(
        f"/inventory-items/{item_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id

    get_response = client.get(
        f"/inventory-items/{item_id}"
    )

    assert get_response.status_code == 404


def test_get_inventory_item_not_found(client):
    response = client.get("/inventory-items/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Inventory item not found"


def test_update_inventory_item_not_found(client):
    response = client.put(
        "/inventory-items/999",
        json={
            "quantity": 1,
            "unit": "kg",
            "status": "started"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Inventory item not found"


def test_delete_inventory_item_not_found(client):
    response = client.delete("/inventory-items/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Inventory item not found"
