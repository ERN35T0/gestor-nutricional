def test_create_prepared_meal(client):
    response = client.post(
        "/prepared-meals",
        json={
            "name": "Sofrito",
            "type": "preparation",
            "quantity": 300,
            "unit": "g",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Sofrito"
    assert data["type"] == "preparation"
    assert data["quantity"] == 300
    assert data["unit"] == "g"
    assert data["recipe_id"] is None


def test_create_prepared_meal_with_recipe(client, create_recipe):
    response = client.post(
        "/prepared-meals",
        json={
            "name": "Lentejas preparadas",
            "type": "meal",
            "quantity": 2,
            "unit": "raciones",
            "recipe_id": create_recipe["id"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Lentejas preparadas"
    assert data["type"] == "meal"
    assert data["recipe_id"] == create_recipe["id"]


def test_create_prepared_meal_without_unit_when_quantity_provided(client):
    response = client.post(
        "/prepared-meals",
        json={
            "name": "Sofrito",
            "type": "preparation",
            "quantity": 300,
        },
    )

    assert response.status_code == 422


def test_get_prepared_meals(client):
    client.post(
        "/prepared-meals",
        json={
            "name": "Sofrito",
            "type": "preparation",
            "quantity": 300,
            "unit": "g",
        },
    )

    response = client.get("/prepared-meals")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Sofrito"


def test_get_prepared_meal(client):
    create_response = client.post(
        "/prepared-meals",
        json={
            "name": "Sofrito",
            "type": "preparation",
            "quantity": 300,
            "unit": "g",
        },
    )

    meal_id = create_response.json()["id"]

    response = client.get(f"/prepared-meals/{meal_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == meal_id
    assert data["name"] == "Sofrito"


def test_get_prepared_meal_not_found(client):
    response = client.get("/prepared-meals/999")

    assert response.status_code == 404


def test_update_prepared_meal(client):
    create_response = client.post(
        "/prepared-meals",
        json={
            "name": "Sofrito",
            "type": "preparation",
            "quantity": 300,
            "unit": "g",
        },
    )

    meal_id = create_response.json()["id"]

    response = client.put(
        f"/prepared-meals/{meal_id}",
        json={
            "name": "Sofrito casero",
            "quantity": 500,
            "unit": "g",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == meal_id
    assert data["name"] == "Sofrito casero"
    assert data["quantity"] == 500
    assert data["unit"] == "g"
    assert data["type"] == "preparation"


def test_update_prepared_meal_not_found(client):
    response = client.put(
        "/prepared-meals/999",
        json={
            "name": "Sofrito",
            "quantity": 300,
            "unit": "g",
        },
    )

    assert response.status_code == 404


def test_delete_prepared_meal(client):
    create_response = client.post(
        "/prepared-meals",
        json={
            "name": "Sofrito",
            "type": "preparation",
            "quantity": 300,
            "unit": "g",
        },
    )

    meal_id = create_response.json()["id"]

    response = client.delete(f"/prepared-meals/{meal_id}")

    assert response.status_code == 200
    assert response.json()["id"] == meal_id

    get_response = client.get(f"/prepared-meals/{meal_id}")

    assert get_response.status_code == 404


def test_delete_prepared_meal_not_found(client):
    response = client.delete("/prepared-meals/999")

    assert response.status_code == 404
