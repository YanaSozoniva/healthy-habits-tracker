from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели пользователя"""

    class Meta:
        model = User
        fields = ("id", "email", "phone", "avatar", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "phone", "avatar")
