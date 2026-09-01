from app.services.meal_suggestion import (
    get_next_meal_suggestion_generation,
)

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
    assert data["status"] == "pending"

def test_meal_suggestion_default_generation(client):
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

    assert data["generation"] == 1


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

def test_generate_meal_suggestions_returns_two(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)

    create_prepared_meal(client)

    response = client.post(
        "/prepared-meals",
        json={
            "name": "Pasta con carne",
            "type": "meal",
            "quantity": 4,
            "unit": "raciones",
        },
    )

    assert response.status_code == 200

    create_prepared_meal(client)

    response = client.post(
        f"/meal-slots/{meal_slot_id}/generate-suggestions"
    )

    assert response.status_code == 200

    suggestions = response.json()

    assert len(suggestions) == 2
    assert all(
        suggestion["meal_slot_id"] == meal_slot_id
        for suggestion in suggestions
    )


def test_generate_meal_suggestions_returns_one_when_only_one_available(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)

    prepared_meal_id = create_prepared_meal(client)

    response = client.post(
        f"/meal-slots/{meal_slot_id}/generate-suggestions"
    )

    assert response.status_code == 200

    suggestions = response.json()

    assert len(suggestions) == 1
    assert suggestions[0]["prepared_meal_id"] == prepared_meal_id


def test_generate_meal_suggestions_returns_empty_when_none_available(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)

    response = client.post(
        f"/meal-slots/{meal_slot_id}/generate-suggestions"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_generate_meal_suggestions_does_not_generate_again_without_rejection(
    client,
):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)

    create_prepared_meal(client)

    response = client.post(
        "/prepared-meals",
        json={
            "name": "Pasta con carne",
            "type": "meal",
            "quantity": 4,
            "unit": "raciones",
        },
    )

    assert response.status_code == 200

    first_response = client.post(
        f"/meal-slots/{meal_slot_id}/generate-suggestions"
    )

    assert first_response.status_code == 200
    assert len(first_response.json()) == 2

    second_response = client.post(
        f"/meal-slots/{meal_slot_id}/generate-suggestions"
    )

    assert second_response.status_code == 400


def test_generate_meal_suggestions_with_invalid_meal_slot(client):
    response = client.post(
        "/meal-slots/999/generate-suggestions"
    )

    assert response.status_code == 404


def test_select_meal_suggestion(client):
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

    response = client.patch(
        f"/meal-suggestions/{suggestion_id}/select"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == suggestion_id
    assert data["status"] == "selected"

def test_reject_meal_suggestion(client):
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

    response = client.patch(
        f"/meal-suggestions/{suggestion_id}/reject"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == suggestion_id
    assert data["status"] == "rejected"

def test_select_rejected_meal_suggestion(client):
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

    reject_response = client.patch(
        f"/meal-suggestions/{suggestion_id}/reject"
    )

    assert reject_response.status_code == 200
    assert reject_response.json()["status"] == "rejected"

    select_response = client.patch(
        f"/meal-suggestions/{suggestion_id}/select"
    )

    assert select_response.status_code == 200
    assert select_response.json()["status"] == "selected"

def test_only_one_meal_suggestion_can_be_selected(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)

    first_prepared_meal_id = create_prepared_meal(client)
    second_prepared_meal_id = create_prepared_meal(client)

    first_response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": meal_slot_id,
            "prepared_meal_id": first_prepared_meal_id,
        },
    )

    second_response = client.post(
        "/meal-suggestions",
        json={
            "meal_slot_id": meal_slot_id,
            "prepared_meal_id": second_prepared_meal_id,
        },
    )

    first_id = first_response.json()["id"]
    second_id = second_response.json()["id"]

    response = client.patch(
        f"/meal-suggestions/{first_id}/select"
    )

    assert response.status_code == 200

    response = client.patch(
        f"/meal-suggestions/{second_id}/select"
    )

    assert response.status_code == 400

def test_next_generation_is_one_when_no_suggestions(db):
    from datetime import date

    from app.models.meal_plan import MealPlan
    from app.models.meal_slot import MealSlot
    from app.services.meal_suggestion import (
        get_next_meal_suggestion_generation,
    )

    meal_plan = MealPlan(
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 7),
    )

    meal_slot = MealSlot(
        date=date(2026, 9, 1),
        meal_type="lunch",
    )

    meal_plan.meal_slots.append(meal_slot)

    db.add(meal_plan)
    db.commit()
    db.refresh(meal_slot)

    generation = get_next_meal_suggestion_generation(
        db,
        meal_slot.id,
    )

    assert generation == 1

def test_next_generation_is_none_when_pending_suggestions_exist(db):
    from datetime import date

    from app.models.meal_plan import MealPlan
    from app.models.meal_slot import MealSlot
    from app.models.meal_suggestion import MealSuggestion
    from app.models.prepared_meal import PreparedMeal
    from app.services.meal_suggestion import (
        get_next_meal_suggestion_generation,
    )

    meal_plan = MealPlan(
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 7),
    )

    meal_slot = MealSlot(
        date=date(2026, 9, 1),
        meal_type="lunch",
    )

    first_meal = PreparedMeal(
        name="Arroz con pollo",
        type="meal",
    )

    second_meal = PreparedMeal(
        name="Pasta con carne",
        type="meal",
    )

    first_suggestion = MealSuggestion(
        prepared_meal=first_meal,
        status="pending",
        generation=1,
    )

    second_suggestion = MealSuggestion(
        prepared_meal=second_meal,
        status="pending",
        generation=1,
    )

    meal_slot.suggestions.extend([
        first_suggestion,
        second_suggestion,
    ])

    meal_plan.meal_slots.append(meal_slot)

    db.add(meal_plan)
    db.commit()

    generation = get_next_meal_suggestion_generation(
        db,
        meal_slot.id,
    )

    assert generation is None

def test_next_generation_is_two_when_first_generation_is_rejected(db):
    from datetime import date

    from app.models.meal_plan import MealPlan
    from app.models.meal_slot import MealSlot
    from app.models.meal_suggestion import MealSuggestion
    from app.models.prepared_meal import PreparedMeal
    from app.services.meal_suggestion import (
        get_next_meal_suggestion_generation,
    )

    meal_plan = MealPlan(
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 7),
    )

    meal_slot = MealSlot(
        date=date(2026, 9, 1),
        meal_type="lunch",
    )

    first_meal = PreparedMeal(
        name="Arroz con pollo",
        type="meal",
    )

    second_meal = PreparedMeal(
        name="Pasta con carne",
        type="meal",
    )

    first_suggestion = MealSuggestion(
        prepared_meal=first_meal,
        status="rejected",
        generation=1,
    )

    second_suggestion = MealSuggestion(
        prepared_meal=second_meal,
        status="rejected",
        generation=1,
    )

    meal_slot.suggestions.extend([
        first_suggestion,
        second_suggestion,
    ])

    meal_plan.meal_slots.append(meal_slot)

    db.add(meal_plan)
    db.commit()

    generation = get_next_meal_suggestion_generation(
        db,
        meal_slot.id,
    )

    assert generation == 2

def test_next_generation_is_none_when_second_generation_exists(db):
    from datetime import date

    from app.models.meal_plan import MealPlan
    from app.models.meal_slot import MealSlot
    from app.models.meal_suggestion import MealSuggestion
    from app.models.prepared_meal import PreparedMeal
    from app.services.meal_suggestion import (
        get_next_meal_suggestion_generation,
    )

    meal_plan = MealPlan(
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 7),
    )

    meal_slot = MealSlot(
        date=date(2026, 9, 1),
        meal_type="lunch",
    )

    meals = [
        PreparedMeal(
            name=f"Comida {index}",
            type="meal",
        )
        for index in range(4)
    ]

    suggestions = [
        MealSuggestion(
            prepared_meal=meals[0],
            status="rejected",
            generation=1,
        ),
        MealSuggestion(
            prepared_meal=meals[1],
            status="rejected",
            generation=1,
        ),
        MealSuggestion(
            prepared_meal=meals[2],
            status="pending",
            generation=2,
        ),
        MealSuggestion(
            prepared_meal=meals[3],
            status="pending",
            generation=2,
        ),
    ]

    meal_slot.suggestions.extend(suggestions)
    meal_plan.meal_slots.append(meal_slot)

    db.add(meal_plan)
    db.commit()

    generation = get_next_meal_suggestion_generation(
        db,
        meal_slot.id,
    )

    assert generation is None


def test_generated_suggestions_have_generation_one(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)

    create_prepared_meal(client)

    response = client.post(
        "/prepared-meals",
        json={
            "name": "Pasta con carne",
            "type": "meal",
        },
    )

    assert response.status_code == 200

    response = client.post(
        f"/meal-slots/{meal_slot_id}/generate-suggestions"
    )

    assert response.status_code == 200

    suggestions = response.json()

    assert len(suggestions) == 2

    assert all(
        suggestion["generation"] == 1
        for suggestion in suggestions
    )

def test_cannot_generate_new_suggestions_when_first_generation_is_pending(
    client,
):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)

    create_prepared_meal(client)

    response = client.post(
        "/prepared-meals",
        json={
            "name": "Pasta con carne",
            "type": "meal",
        },
    )

    assert response.status_code == 200

    first_response = client.post(
        f"/meal-slots/{meal_slot_id}/generate-suggestions"
    )

    assert first_response.status_code == 200

    second_response = client.post(
        f"/meal-slots/{meal_slot_id}/generate-suggestions"
    )

    assert second_response.status_code == 400


def test_can_generate_second_generation_after_rejecting_first(client):
    meal_plan_id = create_meal_plan(client)
    meal_slot_id = create_meal_slot(client, meal_plan_id)

    first_meal_id = create_prepared_meal(client)

    response = client.post(
        "/prepared-meals",
        json={
            "name": "Pasta con carne",
            "type": "meal",
        },
    )
    assert response.status_code == 200
    second_meal_id = response.json()["id"]

    response = client.post(
        "/prepared-meals",
        json={
            "name": "Arroz con pollo",
            "type": "meal",
        },
    )
    assert response.status_code == 200
    third_meal_id = response.json()["id"]

    response = client.post(
        "/prepared-meals",
        json={
            "name": "Wraps de pollo",
            "type": "meal",
        },
    )
    assert response.status_code == 200
    fourth_meal_id = response.json()["id"]

    # Primera generación
    first_response = client.post(
        f"/meal-slots/{meal_slot_id}/generate-suggestions"
    )

    assert first_response.status_code == 200

    first_generation = first_response.json()

    assert len(first_generation) == 2

    first_generation_ids = {
        suggestion["prepared_meal_id"]
        for suggestion in first_generation
    }

    # Rechazamos las dos primeras propuestas
    for suggestion in first_generation:
        response = client.patch(
            f"/meal-suggestions/{suggestion['id']}/reject"
        )

        assert response.status_code == 200

    # Segunda generación
    second_response = client.post(
        f"/meal-slots/{meal_slot_id}/generate-suggestions"
    )

    assert second_response.status_code == 200

    second_generation = second_response.json()

    assert len(second_generation) == 2

    second_generation_ids = {
        suggestion["prepared_meal_id"]
        for suggestion in second_generation
    }

    # Las nuevas propuestas no pueden repetir ninguna de las rechazadas
    assert first_generation_ids.isdisjoint(second_generation_ids)
