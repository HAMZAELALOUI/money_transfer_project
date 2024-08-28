from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from users.permissions import IsOwnerOrAdmin
from users.serializers import UserSerializer
from users.services import UserService


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return super().get_permissions()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            phone_number=serializer.validated_data["phone_number"],
            user_type=serializer.validated_data["user_type"],
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def change_user_type(self, request, pk=None):
        user = self.get_object()
        new_user_type = request.data.get("user_type")
        if new_user_type not in dict(User.USER_TYPES).keys():
            return Response(
                {"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST
            )
        updated_user = UserService.update_user_type(user, new_user_type)
        return Response(UserSerializer(updated_user).data)
