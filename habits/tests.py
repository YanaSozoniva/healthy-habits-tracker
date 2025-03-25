from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.validators import associated_habit_or_reward_validator, associated_habit_is_nice_habit_validator, \
    is_nice_habit_validator
from users.models import User


class HabitsTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="test@sky.pro")
        self.client.force_authenticate(user=self.user)

    def test_habits_list(self):
        """Тестирование вывода списка привычек пользователя"""
        Habit.objects.create(
            periodicity=2,
            date_last_execution="2025-03-24",
            place="дома",
            name="привычка 1",
            action="Проверка",
            lead_time="09:14:00",
            owner=self.user,
        )
        Habit.objects.create(
            periodicity=2,
            date_last_execution="2025-03-24",
            place="дома",
            name="привычка 2",
            action="Проверка",
            lead_time="09:14:00",
            owner=self.user,
        )
        url = reverse("habits:habit_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), 2)

    def test_habits_public_list(self):
        """Тестирование вывода списка публичных привычек"""
        Habit.objects.create(
            periodicity=2,
            date_last_execution="2025-03-24",
            place="дома",
            name="привычка 1",
            action="Проверка",
            lead_time="09:14:00",
            owner=self.user,
        )
        Habit.objects.create(
            periodicity=2,
            date_last_execution="2025-03-24",
            place="дома",
            name="привычка публичная",
            action="Проверка",
            lead_time="09:14:00",
            owner=self.user,
            is_public=True
        )
        url = reverse("habits:habit_public_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), 1)
        self.assertEqual(response.json().get('results')[0].get('name'), "привычка публичная")

    def test_create_habit(self):
        """Тестирование создания полезной привычки"""
        data = {
            "date_last_execution": "2025-03-24",
            "place": "телеграмме",
            "name": "Создание привычки",
            "owner": self.user.pk,
        }
        url = reverse("habits:habit_create")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 1)
        habit = Habit.objects.get(name="Создание привычки")
        self.assertEqual(habit.name, "Создание привычки")

    def test_delete_habit(self):
        """Тестирование удаления полезной привычки"""
        habit = Habit.objects.create(
            periodicity=2,
            date_last_execution="2025-03-24",
            place="дома",
            name="привычка 1",
            action="Проверка",
            lead_time="09:14:00",
            owner=self.user,
        )
        url = reverse("habits:habit_delete", args=(habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_retrieve_habit(self):
        """Тестирование вывода информации по полезной привычке"""
        habit = Habit.objects.create(
            periodicity=2,
            date_last_execution="2025-03-24",
            place="дома",
            name="привычка 1",
            action="Проверка",
            lead_time="09:14:00",
            owner=self.user,
        )
        url = reverse("habits:habit_detail", args=(habit.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("name"), "привычка 1")

    class HabitSerializerTest(TestCase):

        def setUp(self):
            self.user = User.objects.create_user(email='test@user.com', password='testpass')

        def test_valid_data(self):
            """ Тестирование сериализатора на валидацию корректных данных """
            data = {
                "date_last_execution": "2025-03-24",
                "place": "телеграмме",
                "name": "Создание привычки",
                "owner": self.user.pk,
            }
            serializer = HabitSerializer(data=data)
            self.assertTrue(serializer.is_valid())

        def test_invalid_data(self):
            """ Тестирование сериализатора на отклонения некорректных данных """
            data = {
                "date_last_execution": "2025-13-24",
                "place": "телеграмме",
                "name": "Создание привычки",
                "lead_time": "25:00",
                "time_to_complete": 200,
                "periodicity": 8,
                "owner": self.user.pk,
            }
            serializer = HabitSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn("date_last_execution", serializer.errors)
            self.assertIn("lead_time", serializer.errors)
            self.assertIn("time_to_complete", serializer.errors)
            self.assertIn("periodicity", serializer.errors)


class RewardAndAssociatedValidatorTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@user.com', password='testpass')

    def test_associated_habit_or_reward_validator(self):
        """ Тестирование проверки валидатора одновременного указания связанной привычки и вознагражения """
        data = {
            'reward': 'Приз',
            'associated_habit': 1
        }
        with self.assertRaisesMessage(Exception,
                                      'Нельзя одновременно указывать связанную привычку и вознаграждение. Выберите что-то одно.'):
            associated_habit_or_reward_validator(data)

    def test_only_reward(self):
        """ Тестирование корректной обработки валидатора при указании только вознаграждения """
        data = {
            'reward': 'Reward',
            'associated_habit': None
        }
        try:
            associated_habit_or_reward_validator(data)
        except Exception as e:
            self.fail(f'Validator raised exception unexpectedly: {e}')

    def test_associated_habit_is_nice_habit_validator(self):
        """ Тестирование проверки валидатора связанной привычки, если не указано, что это приятная привычка """
        data = {
            'is_nice_habit': False,
            'associated_habit': 1
        }
        with self.assertRaisesMessage(Exception,
                                      'В связанные привычки могут попадать только привычки с признаком приятной привычки'):
            associated_habit_is_nice_habit_validator(data)

    def test_is_nice_habit_validator(self):
        """ Тестирование проверки валидатора, который проверяет, что у приятной привычки нет ни вознаграждения, ни связвнной привычки """
        data = {
            'is_nice_habit': True,
            'reward': 'Reward',
            'associated_habit': 1
        }
        with self.assertRaisesMessage(Exception,
                                      'У приятной привычки не может быть вознаграждения или связанной привычки'):
            is_nice_habit_validator(data)
