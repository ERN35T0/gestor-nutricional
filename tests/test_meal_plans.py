def test_create_meal_plan(client):
    response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] is not None
    assert data["start_date"] == "2026-08-10"
    assert data["end_date"] == "2026-08-16"
    assert data["created_at"] is not None


def test_create_meal_plan_with_invalid_dates(client):
    response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-16",
            "end_date": "2026-08-10",
        },
    )

    assert response.status_code == 422


def test_get_meal_plans(client):
    client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    response = client.get("/meal-plans")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["start_date"] == "2026-08-10"
    assert data[0]["end_date"] == "2026-08-16"


def test_get_meal_plan(client):
    create_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    plan_id = create_response.json()["id"]

    response = client.get(f"/meal-plans/{plan_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == plan_id
    assert data["start_date"] == "2026-08-10"
    assert data["end_date"] == "2026-08-16"


def test_get_meal_plan_not_found(client):
    response = client.get("/meal-plans/999")

    assert response.status_code == 404


def test_update_meal_plan(client):
    create_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    plan_id = create_response.json()["id"]

    response = client.put(
        f"/meal-plans/{plan_id}",
        json={
            "start_date": "2026-08-17",
            "end_date": "2026-08-23",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == plan_id
    assert data["start_date"] == "2026-08-17"
    assert data["end_date"] == "2026-08-23"


def test_update_meal_plan_not_found(client):
    response = client.put(
        "/meal-plans/999",
        json={
            "start_date": "2026-08-17",
            "end_date": "2026-08-23",
        },
    )

    assert response.status_code == 404


def test_update_meal_plan_with_invalid_dates(client):
    create_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    plan_id = create_response.json()["id"]

    response = client.put(
        f"/meal-plans/{plan_id}",
        json={
            "start_date": "2026-08-23",
            "end_date": "2026-08-17",
        },
    )

    assert response.status_code == 422


def test_delete_meal_plan(client):
    create_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    plan_id = create_response.json()["id"]

    response = client.delete(f"/meal-plans/{plan_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == plan_id

    get_response = client.get(f"/meal-plans/{plan_id}")

    assert get_response.status_code == 404


def test_delete_meal_plan_not_found(client):
    response = client.delete("/meal-plans/999")

    assert response.status_code == 404
