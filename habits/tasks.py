from celery import shared_task
from django.utils import timezone
from datetime import timedelta


from habits.services import send_telegram_message
from habits.models import Habit


@shared_task
def send_info_about_habit():
    """ Отправляет пользователю сообщение о том, в какое время какие привычки необходимо выполнять """
    time_now = timezone.now() + timedelta(minutes=5)
    time = time_now.time().replace(second=0, microsecond=0)
    habits = Habit.objects.filter(is_nice_habit=False, lead_time=time)
    print(habits)

    for habit in habits:
        message = f'Я буду {habit.action} в {habit.lead_time} в {habit.place}'
        if habit.owner.tg_chat_id:
            send_telegram_message(habit.owner.tg_chat_id, message)
