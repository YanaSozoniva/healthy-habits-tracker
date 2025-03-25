from rest_framework import serializers

from habits.models import Habit


def associated_habit_or_reward_validator(value):
    """Валидатор для проверки, что нельзя указывать одновременно связанную привычку и вознаграждение."""

    associated_habit = dict(value).get("associated_habit")
    reward = dict(value).get("reward")

    if associated_habit and reward:
        raise serializers.ValidationError(
            "Нельзя одновременно указывать связанную привычку и вознаграждение. Выберите что-то одно."
        )


def associated_habit_is_nice_habit_validator(value):
    """
    Валидатор для проверки, что в связанные привычки могут попадать только привычки с признаком приятной привычки.
    """

    associated_habit = dict(value).get("associated_habit")
    is_nice_habit = dict(value).get("is_nice_habit")

    if associated_habit and not is_nice_habit:
        raise serializers.ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки"
        )


def is_nice_habit_validator(value):
    """Валидатор для проверки, что у приятной привычки не может быть вознаграждения или связанной привычки."""

    nice_habit = dict(value).get("is_nice_habit")
    reward = dict(value).get("reward")
    associated_habit = dict(value).get("associated_habit")

    if nice_habit and reward or associated_habit:
        raise serializers.ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")
