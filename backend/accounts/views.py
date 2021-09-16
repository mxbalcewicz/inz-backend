from .serializers import UserSerializer, UserRegisterSerializer
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework_simplejwt import authentication
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status


class ListUsers(RetrieveAPIView):
    """
    Admin only view to retrieve users in the system
    """
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer(many=True)


class RegisterDeanAccountView(CreateAPIView):
    """
    Register view for dean's account registration
    """
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.create(validated_data=serializer.data, is_dean=True)

        return Response(status=status.HTTP_201_CREATED)


class RegisterStaffAccountView(CreateAPIView):
    """
    Register view for staff's account registration
    """
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.create(validated_data=serializer.data, is_staff=True)

        return Response(status=status.HTTP_201_CREATED)