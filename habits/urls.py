from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (HabitCreateAPIView, HabitDestroyAPIView, HabitListAPIView, HabitRetrieveAPIView,
                          HabitUpdateAPIView)

app_name = HabitsConfig.name

urlpatterns = [
    path("habit/", HabitListAPIView.as_view(), name="habit_list"),
    path("habit/create", HabitCreateAPIView.as_view(), name="habit_create"),
    path("habit/<int:pk>/detail", HabitRetrieveAPIView.as_view(), name="habit_detail"),
    path("habit/<int:pk>/update", HabitUpdateAPIView.as_view(), name="habit_update"),
    path("habit/<int:pk>/delete", HabitDestroyAPIView.as_view(), name="habit_delete"),
]
