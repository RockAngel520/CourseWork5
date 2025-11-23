from django.core.exceptions import ValidationError


def validate_habit(habit):
    """Валидация привычек"""

    if habit.associated_habit and habit.reward:
        raise ValidationError("Запрещен одновременный выбор связанной привычки и указания вознаграждения.")

    if habit.time_to_complete > 120:
        raise ValidationError("Время выполнения должно быть не больше 120 секунд.")

    if habit.associated_habit and not habit.associated_habit.is_pleasant:
        raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки.")

    if habit.is_pleasant and (habit.associated_habit or habit.reward):
        raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

    if not 1 <= habit.period <= 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
