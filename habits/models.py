from django.db import models

from users.models import User


class Habit(models.Model):
    """ Модель Привычка """

    DAILY = "daily"
    ONCE_WEEK = "once_week"
    TWICE_WEEK = "twice_week"
    THREE_WEEK = "three_week"
    FOUR_WEEK = "four_week"
    FIVE_WEEK = "five_week"
    SIX_WEEK = "six_week"

    PERIODICITY_CHOICES = [
        (DAILY, "Ежедневно"),
        (ONCE_WEEK, "1 раз в неделю"),
        (TWICE_WEEK, "2 раза в неделю"),
        (THREE_WEEK, "3 раза в неделю"),
        (FOUR_WEEK, "4 раза в неделю"),
        (FIVE_WEEK, "5 раз в неделю"),
        (SIX_WEEK, "6 раз в неделю"),
    ]

    place = models.CharField(
        max_length=150,
        verbose_name="Место",
        help_text="Укажите место выполнения привычки",
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Название привычки",
        help_text="Укажите название привычки",
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='habits',
        null=True,
        blank=True
    )

    action = models.TextField(
        verbose_name="Действие",
        help_text="Укажите действие, которое представляет собой привычка",
        null=True,
        blank=True
    )

    lead_time = models.DateTimeField(
        verbose_name="Время",
        help_text="Укажите в какое время планируется выполнять привычку",
        null=True,
        blank=True
    )

    associated_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Укажите связанную привычку",
        null=True,
        blank=True
    )

    is_nice_habit = models.BooleanField(
        verbose_name="Признак приятной привычки",
        default=False,
    )

    periodicity = models.CharField(
        max_length=20,
        choices=PERIODICITY_CHOICES,
        default=DAILY,
        verbose_name='Периодичность'
    )

    reward = models.CharField(
        max_length=100,
        verbose_name="Вознаграждение",
        help_text="Чем Вы хотите себя порадовать?",
        null=True,
        blank=True
    )

    time_to_complete = models.PositiveIntegerField(
        verbose_name="Время на выполнение в секундах",
        help_text="Укажите время на выполнения полезной привычки",
        null=True,
        blank=True
    )

    is_public = models.BooleanField(
        verbose_name="Публиковать привычку",
        default=False,
    )
