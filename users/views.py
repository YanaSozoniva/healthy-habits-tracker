from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserDetailSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return UserDetailSerializer
        return UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data["password"])
        user.save()
