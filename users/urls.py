from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from django.urls import path

from users.views import UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("")
] + router.urls
