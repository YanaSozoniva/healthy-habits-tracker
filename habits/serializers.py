from rest_framework import serializers

from habits.models import Habit
from habits.validators import (associated_habit_is_nice_habit_validator, associated_habit_or_reward_validator,
                               is_nice_habit_validator)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели привычка"""

    class Meta:
        model = Habit
        fields = "__all__"
        validators = (
            associated_habit_is_nice_habit_validator,
            associated_habit_or_reward_validator,
            is_nice_habit_validator,
        )
