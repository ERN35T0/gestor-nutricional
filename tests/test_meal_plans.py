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

def test_create_meal_plan_starts_as_draft(client):
    response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "draft"


def test_cannot_confirm_meal_plan_without_slots(client):
    create_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    plan_id = create_response.json()["id"]

    response = client.post(
        f"/meal-plans/{plan_id}/confirm"
    )

    assert response.status_code == 400


def test_cannot_confirm_meal_plan_with_unselected_slot(client):
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

    assert slot_response.status_code == 200

    slot_id = slot_response.json()["id"]

    prepared_meal_response = client.post(
        "/prepared-meals",
        json={
            "name": "Arroz con pollo",
            "type": "meal",
        },
    )

    assert prepared_meal_response.status_code == 200

    prepared_meal_id = prepared_meal_response.json()["id"]

    suggestion_response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": slot_id,
            "prepared_meal_id": prepared_meal_id,
        },
    )

    assert suggestion_response.status_code == 200

    response = client.post(
        f"/meal-plans/{plan_id}/confirm"
    )

    assert response.status_code == 400


def test_can_confirm_meal_plan_when_all_slots_are_selected(client):
    create_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    plan_id = create_response.json()["id"]

    first_slot_response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": plan_id,
            "date": "2026-08-10",
            "meal_type": "lunch",
        },
    )

    assert first_slot_response.status_code == 200

    first_slot_id = first_slot_response.json()["id"]

    second_slot_response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": plan_id,
            "date": "2026-08-11",
            "meal_type": "dinner",
        },
    )

    assert second_slot_response.status_code == 200

    second_slot_id = second_slot_response.json()["id"]

    first_meal_response = client.post(
        "/prepared-meals",
        json={
            "name": "Arroz con pollo",
            "type": "meal",
        },
    )

    assert first_meal_response.status_code == 200

    first_meal_id = first_meal_response.json()["id"]

    second_meal_response = client.post(
        "/prepared-meals",
        json={
            "name": "Pasta con carne",
            "type": "meal",
        },
    )

    assert second_meal_response.status_code == 200

    second_meal_id = second_meal_response.json()["id"]

    first_suggestion_response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": first_slot_id,
            "prepared_meal_id": first_meal_id,
        },
    )

    assert first_suggestion_response.status_code == 200

    first_suggestion_id = first_suggestion_response.json()["id"]

    second_suggestion_response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": second_slot_id,
            "prepared_meal_id": second_meal_id,
        },
    )

    assert second_suggestion_response.status_code == 200

    second_suggestion_id = second_suggestion_response.json()["id"]

    first_select_response = client.patch(
        f"/meal-suggestions/{first_suggestion_id}/select"
    )

    assert first_select_response.status_code == 200

    second_select_response = client.patch(
        f"/meal-suggestions/{second_suggestion_id}/select"
    )

    assert second_select_response.status_code == 200

    response = client.post(
        f"/meal-plans/{plan_id}/confirm"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == plan_id
    assert data["status"] == "confirmed"


def test_cannot_update_confirmed_meal_plan(client):
    create_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    plan_id = create_response.json()["id"]

    # El plan necesita al menos un slot seleccionado para poder confirmarse.
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

    update_response = client.put(
        f"/meal-plans/{plan_id}",
        json={
            "start_date": "2026-08-11",
            "end_date": "2026-08-17",
        },
    )

    assert update_response.status_code == 400
