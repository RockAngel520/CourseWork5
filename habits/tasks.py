import json

import requests
from celery import shared_task
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from config.settings import TG_API_KEY
from habits.models import Habit


@shared_task
def create_periodic_task():

    habits = Habit.objects.all()

    for habit in habits:
        task_name = f"habit_{habit.id}_chat_{habit.user.telegram_chat_id}"

        if not PeriodicTask.objects.filter(name=task_name).exists():
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=habit.period,
                period=IntervalSchedule.DAYS,
            )

            text = f"я буду {habit.action} в {habit.time} в {habit.place}"

            PeriodicTask.objects.create(
                interval=schedule,
                name=task_name,
                task="habits.tasks.send_message",
                args=json.dumps([text, habit.user.telegram_chat_id]),
                start_time=timezone.now() + timezone.timedelta(minutes=1),
            )


@shared_task
def send_message(text, telegram_chat_id):
    params = {"chat_id": telegram_chat_id, "text": text}
    requests.get(f"https://api.telegram.org/bot{TG_API_KEY}/sendMessage", params=params).json()
