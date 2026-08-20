def test_create_product(client):
    response = client.post(
        "/products",
        json={
            "name": "Arroz basmati"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Arroz basmati"
