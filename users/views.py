from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import RegistrationSerializer, UpdateUserSerializer, UserSerializer


@permission_classes([AllowAny])
class RegisterView(CreateAPIView):
    serializer_class = RegistrationSerializer


class UserAccountView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete the user profile"""

    serializer_class = UserSerializer

    @swagger_auto_schema(operation_summary="Получение профиля текущего пользователя", responses={200: UserSerializer()})
    def get_object(self):
        """Retrieve the current user's profile"""

        return self.request.user

    @swagger_auto_schema(
        operation_summary="Обновление профиля пользователя",
        request_body=UpdateUserSerializer,
        responses={200: UserSerializer(), 400: 'Bad Request'},
    )
    def patch(self, request, *args, **kwargs):
        """Edit profile (first_name, last_name)"""

        user = self.get_object()
        serializer = UpdateUserSerializer(self.get_object(), data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Деактивация аккаунта пользователя", responses={204: 'No Content'})
    def delete(self, request, *args, **kwargs):
        """Deactivate account"""

        user = self.get_object()

        user.is_active = False
        user.save(update_fields=["is_active"])

        return Response(status=status.HTTP_204_NO_CONTENT)
