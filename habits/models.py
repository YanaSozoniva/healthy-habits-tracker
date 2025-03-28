from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Habit(models.Model):
    """Модель Привычка"""

    periodicity = models.PositiveIntegerField(
        validators=[MaxValueValidator(7), MinValueValidator(1)],
        default=1,
        verbose_name="Периодичность",
        help_text="Выберите через сколько дней будите выполнять полезную привычку (1-7)",
    )
    date_last_execution = models.DateField(
        verbose_name="Дата последнего выполнения полезной привычки", null=True, blank=True
    )

    place = models.CharField(
        max_length=150, verbose_name="Место", help_text="Укажите место выполнения привычки", null=True, blank=True
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Название привычки",
        help_text="Укажите название привычки",
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits", null=True, blank=True)

    action = models.TextField(
        verbose_name="Действие",
        help_text="Укажите действие, которое представляет собой привычка",
        null=True,
        blank=True,
    )

    lead_time = models.TimeField(
        verbose_name="Время", help_text="Укажите в какое время планируется выполнять привычку", null=True, blank=True
    )

    associated_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Укажите связанную привычку",
        null=True,
        blank=True,
    )

    is_nice_habit = models.BooleanField(
        verbose_name="Признак приятной привычки",
        default=False,
    )

    reward = models.CharField(
        max_length=100,
        verbose_name="Вознаграждение",
        help_text="Чем Вы хотите себя порадовать?",
        null=True,
        blank=True,
    )

    time_to_complete = models.PositiveIntegerField(
        validators=[MaxValueValidator(120)],
        verbose_name="Время на выполнение в секундах",
        help_text="Укажите время на выполнения полезной привычки",
        null=True,
        blank=True,
    )

    is_public = models.BooleanField(
        verbose_name="Публиковать привычку",
        default=False,
    )
