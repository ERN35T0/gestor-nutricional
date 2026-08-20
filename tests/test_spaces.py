def test_create_space(client):
    response = client.post(
        "/spaces",
        json={
            "name": "Casa"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Casa"
    assert "id" in data


def test_get_spaces(client):
    response = client.post(
        "/spaces",
        json={
            "name": "Casa"
        }
    )

    assert response.status_code == 200

    response = client.get("/spaces")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Casa"


def test_get_space(client):
    response = client.post(
        "/spaces",
        json={
            "name": "Casa"
        }
    )

    assert response.status_code == 200

    space_id = response.json()["id"]

    response = client.get(
        f"/spaces/{space_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == space_id
    assert data["name"] == "Casa"


def test_update_space(client):
    response = client.post(
        "/spaces",
        json={
            "name": "Casa"
        }
    )

    assert response.status_code == 200

    space_id = response.json()["id"]

    response = client.put(
        f"/spaces/{space_id}",
        json={
            "name": "Vacaciones"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == space_id
    assert data["name"] == "Vacaciones"

