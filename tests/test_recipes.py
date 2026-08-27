def test_create_recipe(client):
    response = client.post(
        "/recipes",
        json={
            "name": "Arroz con pollo"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Arroz con pollo"


def test_get_recipes(client):
    client.post(
        "/recipes",
        json={
            "name": "Arroz con pollo"
        }
    )

    client.post(
        "/recipes",
        json={
            "name": "Ensalada de garbanzos"
        }
    )

    response = client.get("/recipes")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Arroz con pollo"
    assert data[1]["name"] == "Ensalada de garbanzos"


def test_get_recipe(client):
    create_response = client.post(
        "/recipes",
        json={
            "name": "Arroz con pollo"
        }
    )

    recipe_id = create_response.json()["id"]

    response = client.get(f"/recipes/{recipe_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == recipe_id
    assert data["name"] == "Arroz con pollo"


def test_get_recipe_not_found(client):
    response = client.get("/recipes/999")

    assert response.status_code == 404


def test_update_recipe(client):
    create_response = client.post(
        "/recipes",
        json={
            "name": "Arroz con pollo"
        }
    )

    recipe_id = create_response.json()["id"]

    response = client.put(
        f"/recipes/{recipe_id}",
        json={
            "name": "Arroz con verduras"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == recipe_id
    assert data["name"] == "Arroz con verduras"


def test_update_recipe_not_found(client):
    response = client.put(
        "/recipes/999",
        json={
            "name": "Receta inexistente"
        }
    )

    assert response.status_code == 404
