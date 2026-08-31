def create_meal_plan(client):
    response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    assert response.status_code == 200

    return response.json()["id"]


def create_meal_slot(client, meal_plan_id):
    response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": meal_plan_id,
            "date": "2026-08-10",
            "meal_type": "lunch",
        },
    )

    assert response.status_code == 200

    return response.json()["id"]


def create_prepared_meal(client):
    response = client.post(
        "/prepared-meals",
        json={
            "name": "Arroz con pollo",
            "type": "meal",
            "quantity": 4,
            "unit": "raciones",
        },
    )

    assert response.status_code == 200

    return response.json()["id"]


def test_create_meal_suggestion(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)
    prepared_meal_id = create_prepared_meal(client)

    response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": meal_slot_id,
            "prepared_meal_id": prepared_meal_id,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] is not None
    assert data["meal_slot_id"] == meal_slot_id
    assert data["prepared_meal_id"] == prepared_meal_id


def test_create_meal_suggestion_with_invalid_meal_slot(client):
    prepared_meal_id = create_prepared_meal(client)

    response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": 999,
            "prepared_meal_id": prepared_meal_id,
        },
    )

    assert response.status_code == 404


def test_create_meal_suggestion_with_invalid_prepared_meal(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)

    response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": meal_slot_id,
            "prepared_meal_id": 999,
        },
    )

    assert response.status_code == 404


def test_get_meal_suggestions(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)
    prepared_meal_id = create_prepared_meal(client)

    client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": meal_slot_id,
            "prepared_meal_id": prepared_meal_id,
        },
    )

    response = client.get("/meal-suggestions")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["meal_slot_id"] == meal_slot_id
    assert data[0]["prepared_meal_id"] == prepared_meal_id


def test_get_meal_suggestion(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)
    prepared_meal_id = create_prepared_meal(client)

    create_response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": meal_slot_id,
            "prepared_meal_id": prepared_meal_id,
        },
    )

    suggestion_id = create_response.json()["id"]

    response = client.get(f"/meal-suggestions/{suggestion_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == suggestion_id
    assert data["meal_slot_id"] == meal_slot_id
    assert data["prepared_meal_id"] == prepared_meal_id


def test_get_meal_suggestion_not_found(client):
    response = client.get("/meal-suggestions/999")

    assert response.status_code == 404


def test_delete_meal_suggestion(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)
    prepared_meal_id = create_prepared_meal(client)

    create_response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": meal_slot_id,
            "prepared_meal_id": prepared_meal_id,
        },
    )

    suggestion_id = create_response.json()["id"]

    response = client.delete(f"/meal-suggestions/{suggestion_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == suggestion_id

    get_response = client.get(f"/meal-suggestions/{suggestion_id}")

    assert get_response.status_code == 404


def test_delete_meal_suggestion_not_found(client):
    response = client.delete("/meal-suggestions/999")

    assert response.status_code == 404


def test_get_meal_suggestions_for_slot(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)
    other_slot_id = create_meal_slot(client, meal_plan_id)

    prepared_meal_id = create_prepared_meal(client)

    response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": meal_slot_id,
            "prepared_meal_id": prepared_meal_id,
        },
    )

    assert response.status_code == 200

    response = client.get(
        f"/meal-slots/{meal_slot_id}/suggestions"
    )

    assert response.status_code == 200

    suggestions = response.json()

    assert len(suggestions) == 1
    assert suggestions[0]["meal_slot_id"] == meal_slot_id

    response = client.get(
        f"/meal-slots/{other_slot_id}/suggestions"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_meal_suggestion_relationships(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)
    prepared_meal_id = create_prepared_meal(client)

    response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": meal_slot_id,
            "prepared_meal_id": prepared_meal_id,
        },
    )

    assert response.status_code == 200

    response = client.get(
        f"/meal-slots/{meal_slot_id}/suggestions"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_meal_slot_relationships(db):
    from datetime import date

    from app.models.meal_plan import MealPlan
    from app.models.meal_slot import MealSlot

    meal_plan = MealPlan(
        start_date=date(2026, 8, 28),
        end_date=date(2026, 8, 30),
    )

    meal_slot = MealSlot(
        date=date(2026, 8, 28),
        meal_type="lunch",
    )

    meal_plan.meal_slots.append(meal_slot)

    db.add(meal_plan)
    db.commit()
    db.refresh(meal_plan)

    assert meal_slot.meal_plan is meal_plan
    assert meal_slot in meal_plan.meal_slots


def test_meal_suggestion_relationships(db):
    from datetime import date

    from app.models.meal_plan import MealPlan
    from app.models.meal_slot import MealSlot
    from app.models.meal_suggestion import MealSuggestion
    from app.models.prepared_meal import PreparedMeal

    meal_plan = MealPlan(
        start_date=date(2026, 8, 28),
        end_date=date(2026, 8, 30),
    )

    meal_slot = MealSlot(
        date=date(2026, 8, 28),
        meal_type="lunch",
    )

    prepared_meal = PreparedMeal(
        name="Arroz con pollo",
        type="meal",
    )

    suggestion = MealSuggestion(
        prepared_meal=prepared_meal,
    )

    meal_slot.suggestions.append(suggestion)
    meal_plan.meal_slots.append(meal_slot)

    db.add(meal_plan)
    db.commit()

    assert suggestion.meal_slot is meal_slot
    assert suggestion.prepared_meal is prepared_meal
    assert suggestion in meal_slot.suggestions
    assert suggestion in prepared_meal.meal_suggestions


def test_relationships_work_after_reload(db):
    from datetime import date

    from app.models.meal_plan import MealPlan
    from app.models.meal_slot import MealSlot
    from app.models.meal_suggestion import MealSuggestion
    from app.models.prepared_meal import PreparedMeal

    meal_plan = MealPlan(
        start_date=date(2026, 8, 28),
        end_date=date(2026, 8, 30),
    )

    meal_slot = MealSlot(
        date=date(2026, 8, 28),
        meal_type="dinner",
    )

    prepared_meal = PreparedMeal(
        name="Pasta con carne",
        type="meal",
    )

    suggestion = MealSuggestion(
        prepared_meal=prepared_meal,
    )

    meal_slot.suggestions.append(suggestion)
    meal_plan.meal_slots.append(meal_slot)

    db.add(meal_plan)
    db.commit()

    meal_plan_id = meal_plan.id
    meal_slot_id = meal_slot.id
    suggestion_id = suggestion.id
    prepared_meal_id = prepared_meal.id

    db.expire_all()

    loaded_plan = db.get(MealPlan, meal_plan_id)
    loaded_slot = db.get(MealSlot, meal_slot_id)
    loaded_suggestion = db.get(MealSuggestion, suggestion_id)
    loaded_prepared_meal = db.get(
        PreparedMeal,
        prepared_meal_id,
    )

    assert loaded_slot.meal_plan.id == loaded_plan.id
    assert loaded_suggestion.meal_slot.id == loaded_slot.id
    assert loaded_suggestion.prepared_meal.id == loaded_prepared_meal.id

    assert loaded_slot in loaded_plan.meal_slots
    assert loaded_suggestion in loaded_slot.suggestions
    assert loaded_suggestion in loaded_prepared_meal.meal_suggestions

def test_create_duplicate_meal_suggestion(client):
    # Creamos una planificación.
    meal_plan_response = client.post(
        "/meal-plans",
        json={
            "start_date": "2026-08-10",
            "end_date": "2026-08-16",
        },
    )

    meal_plan_id = meal_plan_response.json()["id"]

    # Creamos un hueco dentro de la planificación.
    meal_slot_response = client.post(
        "/meal-slots",
        json={
            "meal_plan_id": meal_plan_id,
            "date": "2026-08-10",
            "meal_type": "breakfast",
        },
    )

    meal_slot_id = meal_slot_response.json()["id"]

    # Creamos una comida preparada que podremos sugerir.
    prepared_meal_response = client.post(
        "/prepared-meals",
        json={
            "name": "Tortilla",
            "type": "meal",
        },
    )

    prepared_meal_id = prepared_meal_response.json()["id"]

    # Primera sugerencia: debe crearse correctamente.
    first_response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": meal_slot_id,
            "prepared_meal_id": prepared_meal_id,
        },
    )

    assert first_response.status_code == 200

    # Segunda sugerencia idéntica: no debería permitirse.
    second_response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": meal_slot_id,
            "prepared_meal_id": prepared_meal_id,
        },
    )

    assert second_response.status_code == 400
