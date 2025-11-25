from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь",
        help_text="Выберите создателя привычки",
    )
    place = models.CharField(max_length=250, verbose_name="Место", help_text="Введите место")
    time = models.TimeField(default="09:00:00", verbose_name="Время", help_text="Укажите время")
    action = models.CharField(max_length=250, verbose_name="Действие", help_text="Введите действие")
    is_pleasant = models.BooleanField(
        verbose_name="Признак приятной привычки", help_text="Является ли " "привычка приятной"
    )
    associated_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_habits",
        verbose_name="Связанная привычка",
        help_text="Введите действие",
    )
    period = models.PositiveIntegerField(default=7, verbose_name="Периодичность")
    reward = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="Вознаграждение", help_text="Введите вознаграждение"
    )
    time_to_complete = models.PositiveIntegerField(
        default=60,
        verbose_name="Время на выполнение в секундах",
        help_text="Укажите время в секундах",
    )
    is_public = models.BooleanField(
        default=False, verbose_name="Признак публичности", help_text="Укажите " "признак публичности"
    )

    def __str__(self):
        return f"{self.action} ({self.user.username})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["action"]
