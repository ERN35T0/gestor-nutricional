class MealSlotDateOutOfRangeError(Exception):
    """
    Se produce cuando la fecha de un MealSlot queda
    fuera del rango de fechas de su MealPlan.
    """
    pass

class MealSuggestionAlreadyExistsError(Exception):
    """
    Se produce cuando se intenta crear una sugerencia
    que ya existe para ese hueco y comida preparada.
    """
    pass

class MealPlanConfirmedError(Exception):

    pass
