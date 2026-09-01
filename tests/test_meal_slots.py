def test_create_meal_slot(client):
    meal_plan_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    meal_plan_id = meal_plan_response.json()["id"]

    response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": meal_plan_id,
            "date": "2026-08-10",
            "meal_type": "breakfast",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] is not None
    assert data["meal_plan_id"] == meal_plan_id
    assert data["date"] == "2026-08-10"
    assert data["meal_type"] == "breakfast"


def test_get_meal_slots(client):
    meal_plan_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    meal_plan_id = meal_plan_response.json()["id"]

    client.post(
        "/meal-slots",
        json={
            "meal_plan_id": meal_plan_id,
            "date": "2026-08-10",
            "meal_type": "breakfast",
        },
    )

    response = client.get("/meal-slots")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["meal_plan_id"] == meal_plan_id
    assert data[0]["date"] == "2026-08-10"
    assert data[0]["meal_type"] == "breakfast"


def test_get_meal_slot(client):
    meal_plan_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    meal_plan_id = meal_plan_response.json()["id"]

    create_response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": meal_plan_id,
            "date": "2026-08-10",
            "meal_type": "breakfast",
        },
    )

    slot_id = create_response.json()["id"]

    response = client.get(f"/meal-slots/{slot_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == slot_id
    assert data["meal_plan_id"] == meal_plan_id
    assert data["date"] == "2026-08-10"
    assert data["meal_type"] == "breakfast"


def test_get_meal_slot_not_found(client):
    response = client.get("/meal-slots/999")

    assert response.status_code == 404


def test_update_meal_slot(client):
    meal_plan_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    meal_plan_id = meal_plan_response.json()["id"]

    create_response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": meal_plan_id,
            "date": "2026-08-10",
            "meal_type": "breakfast",
        },
    )

    slot_id = create_response.json()["id"]

    response = client.put(
        f"/meal-slots/{slot_id}",
        json={
            "date": "2026-08-10",
            "meal_type": "lunch",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == slot_id
    assert data["meal_plan_id"] == meal_plan_id
    assert data["date"] == "2026-08-10"
    assert data["meal_type"] == "lunch"


def test_update_meal_slot_not_found(client):
    response = client.put(
        "/meal-slots/999",
        json={
            "date": "2026-08-10",
            "meal_type": "lunch",
        },
    )

    assert response.status_code == 404


def test_delete_meal_slot(client):
    meal_plan_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    meal_plan_id = meal_plan_response.json()["id"]

    create_response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": meal_plan_id,
            "date": "2026-08-10",
            "meal_type": "breakfast",
        },
    )

    slot_id = create_response.json()["id"]

    response = client.delete(f"/meal-slots/{slot_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == slot_id

    get_response = client.get(f"/meal-slots/{slot_id}")

    assert get_response.status_code == 404


def test_delete_meal_slot_not_found(client):
    response = client.delete("/meal-slots/999")

    assert response.status_code == 404

def test_create_meal_slot_with_invalid_meal_plan(client):
    response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": 999,
            "date": "2026-08-10",
            "meal_type": "breakfast",
        },
    )

    assert response.status_code == 404

def test_create_meal_slot_before_meal_plan_start_date(client):
    meal_plan_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    meal_plan_id = meal_plan_response.json()["id"]

    response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": meal_plan_id,
            "date": "2026-08-09",
            "meal_type": "breakfast",
        },
    )

    assert response.status_code == 400


def test_create_meal_slot_after_meal_plan_end_date(client):
    meal_plan_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    meal_plan_id = meal_plan_response.json()["id"]

    response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": meal_plan_id,
            "date": "2026-08-17",
            "meal_type": "breakfast",
        },
    )

    assert response.status_code == 400

def test_update_meal_slot_before_meal_plan_start_date(client):
    meal_plan_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    meal_plan_id = meal_plan_response.json()["id"]

    create_response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": meal_plan_id,
            "date": "2026-08-10",
            "meal_type": "breakfast",
        },
    )

    slot_id = create_response.json()["id"]

    response = client.put(
        f"/meal-slots/{slot_id}",
        json={
            "date": "2026-08-09",
            "meal_type": "breakfast",
        },
    )

    assert response.status_code == 400


def test_update_meal_slot_after_meal_plan_end_date(client):
    meal_plan_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    meal_plan_id = meal_plan_response.json()["id"]

    create_response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": meal_plan_id,
            "date": "2026-08-10",
            "meal_type": "breakfast",
        },
    )

    slot_id = create_response.json()["id"]

    response = client.put(
        f"/meal-slots/{slot_id}",
        json={
            "date": "2026-08-17",
            "meal_type": "breakfast",
        },
    )

    assert response.status_code == 400

def test_cannot_create_meal_slot_in_confirmed_meal_plan(client):
    create_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    plan_id = create_response.json()["id"]

    # Creamos y seleccionamos un slot para poder confirmar el plan.
    slot_response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": plan_id,
            "date": "2026-08-10",
            "meal_type": "lunch",
        },
    )

    slot_id = slot_response.json()["id"]

    meal_response = client.post(
        "/prepared-meals",
        json={
            "name": "Arroz con pollo",
            "type": "meal",
        },
    )

    meal_id = meal_response.json()["id"]

    suggestion_response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": slot_id,
            "prepared_meal_id": meal_id,
        },
    )

    suggestion_id = suggestion_response.json()["id"]

    select_response = client.patch(
        f"/meal-suggestions/{suggestion_id}/select"
    )

    assert select_response.status_code == 200

    confirm_response = client.post(
        f"/meal-plans/{plan_id}/confirm"
    )

    assert confirm_response.status_code == 200

    response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": plan_id,
            "date": "2026-08-11",
            "meal_type": "dinner",
        },
    )

    assert response.status_code == 400


def test_cannot_update_meal_slot_in_confirmed_meal_plan(client):
    create_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    plan_id = create_response.json()["id"]

    slot_response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": plan_id,
            "date": "2026-08-10",
            "meal_type": "lunch",
        },
    )

    slot_id = slot_response.json()["id"]

    meal_response = client.post(
        "/prepared-meals",
        json={
            "name": "Arroz con pollo",
            "type": "meal",
        },
    )

    meal_id = meal_response.json()["id"]

    suggestion_response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": slot_id,
            "prepared_meal_id": meal_id,
        },
    )

    suggestion_id = suggestion_response.json()["id"]

    select_response = client.patch(
        f"/meal-suggestions/{suggestion_id}/select"
    )

    assert select_response.status_code == 200

    confirm_response = client.post(
        f"/meal-plans/{plan_id}/confirm"
    )

    assert confirm_response.status_code == 200

    response = client.put(
        f"/meal-slots/{slot_id}",
        json={
            "date": "2026-08-11",
            "meal_type": "dinner",
        },
    )

    assert response.status_code == 400


def test_cannot_delete_meal_slot_from_confirmed_meal_plan(client):
    create_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    plan_id = create_response.json()["id"]

    slot_response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": plan_id,
            "date": "2026-08-10",
            "meal_type": "lunch",
        },
    )

    slot_id = slot_response.json()["id"]

    meal_response = client.post(
        "/prepared-meals",
        json={
            "name": "Arroz con pollo",
            "type": "meal",
        },
    )

    meal_id = meal_response.json()["id"]

    suggestion_response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": slot_id,
            "prepared_meal_id": meal_id,
        },
    )

    suggestion_id = suggestion_response.json()["id"]

    select_response = client.patch(
        f"/meal-suggestions/{suggestion_id}/select"
    )

    assert select_response.status_code == 200

    confirm_response = client.post(
        f"/meal-plans/{plan_id}/confirm"
    )

    assert confirm_response.status_code == 200

    response = client.delete(
        f"/meal-slots/{slot_id}"
    )

    assert response.status_code == 400
