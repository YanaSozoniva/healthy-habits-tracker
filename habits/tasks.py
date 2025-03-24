from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_info_about_habit():
    """Отправляет пользователю сообщение о том, в какое время какие привычки необходимо выполнять"""
    date_now = timezone.now().date()
    time_now = timezone.now() + timedelta(minutes=5)
    time = time_now.time().replace(second=0, microsecond=0)
    habits = Habit.objects.filter(is_nice_habit=False, lead_time=time, date_last_execution=date_now)
    print(habits)

    for habit in habits:
        days = habit.periodicity
        habit.date_last_execution = date_now + timedelta(days=days)
        habit.save()

        message = (f"Я буду {habit.action} в {habit.lead_time} в {habit.place}. После сможете себя порадовать "
                   f"{habit.associated_habit if habit.associated_habit else habit.reward}")
        if habit.owner.tg_chat_id:
            send_telegram_message(habit.owner.tg_chat_id, message)

