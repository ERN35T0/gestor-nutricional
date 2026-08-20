def test_create_product(client):
    response = client.post(
        "/products",
        json={
            "name": "Arroz basmati"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Arroz basmati"

def test_get_products(client):
    response = client.post(
        "/products",
        json={
            "name": "Arroz basmati"
        }
    )

    assert response.status_code == 200

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Arroz basmati"


def test_get_product(client):
    response = client.post(
        "/products",
        json={
            "name": "Pasta integral"
        }
    )

    assert response.status_code == 200

    product_id = response.json()["id"]

    response = client.get(
        f"/products/{product_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Pasta integral"


def test_update_product(client):
    response = client.post(
        "/products",
        json={
            "name": "Arroz blanco"
        }
    )

    assert response.status_code == 200

    product_id = response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Arroz integral"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Arroz integral"
