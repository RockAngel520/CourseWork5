from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="123", telegram_chat_id="123456789")
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Выпить воды",
            is_pleasant=False,
            associated_habit=None,
            period=1,
            reward=None,
            time_to_complete=10,
            is_public=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        url = reverse("habits:habits-list")
        data = {
            "place": "Офис",
            "time": "10:00:00",
            "action": "Разминка",
            "is_pleasant": False,
            "period": 1,
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_list(self):
        url = reverse("habits:habits-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results", [])), 1)

    def test_habit_update(self):
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        data = {"action": "Поднятие гантелей"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Поднятие гантелей")

    def test_habit_delete(self):
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_user_not_authenticate(self):
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
