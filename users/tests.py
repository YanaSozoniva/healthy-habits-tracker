from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.validators import associated_habit_or_reward_validator, associated_habit_is_nice_habit_validator
from users.models import User


class UserTest(APITestCase):
    def setUp(self) -> None:
       pass

    def test_create_user(self):
        data = {
            "email": "test@test.com",
            "password": "test",
        }

        response = self.client.post("/users/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
