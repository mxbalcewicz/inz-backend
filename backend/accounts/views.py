from .serializers import UserSerializer, DeanRegisterSerializer, StaffRegisterSerializer
from .models import DeaneryAccount
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
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


class DeanRegisterView(APIView):
    """
    DeaneryAccount register view
    """
    serializer_class = DeanRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StaffRegisterView(APIView):
    """
    StaffAccount register view
    """
    serializer_class = StaffRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)